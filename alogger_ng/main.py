#! /usr/bin/env python

"""

To Configure this program see alogger-ng.cfg

To customise this to read a different log format
just implement a method like pbs_to_dict (see below)

"""

MAX_JOB_LENGTH = 94608000 # 3 years

import sys, os
import datetime
from accounts.main.models import *
from accounts.alogger_ng.core import log_to_dict, get_in_seconds, print_error


DEBUG = False

    
"""
Assumes the file name is in the format YYYYMMDD

"""

def parse_logs(log_list, date, machine_name, log_type):
    """
    filename format YYYYMMDD
    
    """
    

    if date == datetime.date.today():
        return "Won't proccess todays logs"
    

    output = []
    count = fail = skip = 0
    line_no = 0

    try:
        machine = Machine.objects.get(name=machine_name)
    except:
        return "ERROR: Couldn't find machine named: %s" % machine_name

    if CPUJob.objects.filter(machine=machine, date=date).count() > 0:
        return "Already done this log file"

    try:
        user_account = UserAccount.objects.get(username='unknown_user', machine_category=machine.category)
    except:
        return "ERROR: Couldn't find unknown_user for machine category %s, please create one" % machine.category.name

    try:
        project = Project.objects.get(pk='Unknown_Project')
    except:
        return "ERROR: Couldn't find project Unknown_Project, please create one"

        
    for line in log_list:
        line_no = line_no + 1
        try:
             data = log_to_dict(line, log_type)
        except ValueError:
            print_error(line_no, "Error reading line")
        except:
            skip = skip + 1
            continue

        try:
            user_account = UserAccount.objects.get(username=data['user'], machine_category=machine.category)
        except:
            # Couldn't find user account - Assign to user 'Unknown_User'
            user_account = UserAccount.objects.get(username='unknown_user', machine_category=machine.category)
            output.append("Couldn't find user account for username=%s and machine category=%s" % (data['user'], machine.category.name))
            fail = fail + 1



        if 'project' in data:
            try:
                project = Project.objects.get(pk=data['project'])
            except:
                try:
                    project = user_account.default_project
                except:
                    output.append(line_no, "Couldn't find specified project: %s" % data['project'])
                    project = Project.objects.get(pk='Unknown_Project')
                    fail = fail + 1

        else:
            try:
                project = user_account.default_project
            except:
                # Couldn't find project - Assign to 'Unknown_Project'
                output.append(line_no, "Couldn't find default project for username=%s and machine category=%s" % (data['user'], machine.category.name))
                project = Project.objects.get(pk='Unknown_Project')
                fail +=  1
                
        if project is None:
            project = Project.objects.get(pk='Unknown_Project')
        
        if user_account.user not in project.users.all():
            output.append(line_no, "%s is not in project %s, cpu usage: %s" % (user_account.user, project, data['cpu_usage']))
            fail += 1

        # Everything is good so add entry
        est_wall_time = data['est_wall_time']
        act_wall_time = data['act_wall_time']
        
        queue, created = Queue.objects.get_or_create(name=data['queue'])
        mem = data['mem']
        vmem = data['vmem']
        ctime = data['ctime']
        qtime = data['qtime']
        etime = data['etime']
        start = data['start']

        try:
            if DEBUG:
                output.append("INSERT: %s, %s, %s, %s, %s" % (str(date), user_account.username, project.pid, machine, data['cpu_usage']))
            else:
                CPUJob.objects.create(
                    user=user_account,
                    username=data['user'],
                    project=project,
                    machine=machine,
                    date=date,
                    queue=queue,
                    cpu_usage=data['cpu_usage'],
                    est_wall_time=data['est_wall_time'],
                    act_wall_time=data['act_wall_time'],
                    mem = data['mem'],
                    vmem = data['vmem'],
                    ctime = data['ctime'],
                    qtime = data['qtime'],
                    etime = data['etime'],
                    start = data['start'],
                )
                    
            count = count + 1
            
        except Exception, e:
            output.append("Failed to insert a line  - %s" % e)
            fail = fail + 1
            continue

    summary = 'Inserted : %i\nFailed   : %i\nSkiped   : %i' % (count, fail, skip)


    if DEBUG:
        print 'Inserted : %i' % count
        print 'Failed   : %i' % fail
        print 'Skiped   : %i' % skip

        
    return summary, output

