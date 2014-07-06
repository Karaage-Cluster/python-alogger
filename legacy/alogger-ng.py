#! /usr/bin/env python

# Copyright 208-2014 VPAC
#
# This file is part of python-alogger.
#
# python-alogger is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-alogger is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with python-alogger  If not, see <http://www.gnu.org/licenses/>.

# Anyone using this code as is deserves to be shot. In the left foot.
# Repeatedly.

"""

To Configure this program see python-alogger.cfg

To customise this to read a different log format
just implement a method like pbs_to_dict (see below)

"""
MAX_JOB_LENGTH = 94608000  # 3 years

import sys
import MySQLdb
import datetime

import ConfigParser
import getopt

try:
    opts, args = getopt.getopt(sys.argv[1:], 'c:f:')
    opts = dict(opts)
    config_file = opts['-c']
    try:
        filename = opts['-f']
        file_option = True
    except:
        file_option = False
except getopt.GetoptError:
    print "Need to define config file with -c option"
    sys.exit(2)

try:
    cfg = ConfigParser.ConfigParser()
    cfg.readfp(open(config_file))
except:
    print "Failed to read config file - %s" % config_file
    sys.exit(2)

try:
    DB_HOST = cfg.get('Default', 'db_host')
    DB_USER = cfg.get('Default', 'db_user')
    DB_PASSWD = cfg.get('Default', 'db_passwd')
    DB_NAME = cfg.get('Default', 'db_name')
    LOG_DIR = cfg.get('Default', 'logs_dir')
    MACHINE_NAME = cfg.get('Default', 'machine_name')
except:
    print "Failed to specify all options in config file"
    sys.exit(2)


"""
Assumes the file name is in the format YYYYMMDD

"""


def print_error(file, date, message):
    """
    Method called when error occurs
    """
    print '%s | %s | %s' % (file, date, message)


def get_user_account(conn, username, machine_cat_id):
    """
    Finds a user account given a username and a
    machine category id.

    returns a user account as a dict

    """

    SQL = "SELECT * FROM user_account " \
        "WHERE username = '%s' AND machine_category_id = '%s'" \
        % (username, machine_cat_id)

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(SQL)
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 1:
        return rows[0]

    raise LookupError


def get_machine(conn, machine_name):
    """
    Finds a machine given a machine name

    returns a machine as a dict
    """

    SQL = "SELECT * FROM machine WHERE name = '%s'" % machine_name

    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(SQL)
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 1:
        return rows[0]

    else:
        raise LookupError


def get_in_seconds(time):
    """
    Takes a string in format HH:MM:SS
    Note hours can be more than 2 digits

    if greater than 3 years

    returns the time in seconds
    """
    hours, minutes, seconds = time.split(':')

    # 26280 = 3 years in hours
    if int(hours) > 26280:
        raise ValueError

    total = int((int(hours)*60*60) + (int(minutes)*60) + int(seconds))

    return total


def get_project(conn, data, default_project):
    # Try and find the project from the log
    if 'project' in data:
        project_id = data['project']
        SQL = "SELECT * FROM project WHERE pid = '%s'" % project_id

        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(SQL)
        rows = cursor.fetchall()
        cursor.close()
        if len(rows) == 1:
            return project_id

    # Need to find default project
    project_id = default_project
    if project_id is not None:
        return project_id

    raise ValueError


def pbs_to_dict(line):
    """
    Parses a PBS log file line into a python dict

    raises KeyError when line not valid
    raises ValueError when time over 3 years

    """

    # Split line into parts, only care about raw_data
    date, random, job_num, raw_data = line.split(';')

    raw_data = raw_data.split(' ')

    data = {}
    formatted_data = {}

    # Make into a dict using values key=value
    for d in raw_data:
        try:
            key, value = d.split('=')
            data[key] = value
        except:
            continue

    # Check to see if line worth proccessing
    if 'resources_used.walltime' not in data:
        raise KeyError

    formatted_data['user'] = data['user']
    if 'account' in data:
        formatted_data['project'] = data['account']

    try:
        formatted_data['est_wall_time'] \
            = int(get_in_seconds(data['Resource_List.walltime']))
        formatted_data['act_wall_time'] \
            = int(get_in_seconds(data['resources_used.walltime']))
    except:
        raise ValueError

    cores = data['exec_host'].count('/')
    formatted_data['cpu_usage'] = cores * formatted_data['act_wall_time']

    formatted_data['queue'] = data['queue']

    # Strip kb fro end of mem entries
    # No mem field for wembley-hp
    try:
        formatted_data['mem'] = \
            int(data['resources_used.mem'][:len(data['resources_used.mem'])-2])
    except:
        formatted_data['mem'] = 0

    formatted_data['vmem'] = \
        int(data['resources_used.vmem'][:len(data['resources_used.vmem'])-2])

    fromtimestamp = datetime.datetime.fromtimestamp
    formatted_data['ctime'] = fromtimestamp(int(data['ctime'])).isoformat(' ')
    formatted_data['qtime'] = fromtimestamp(int(data['qtime'])).isoformat(' ')
    formatted_data['etime'] = fromtimestamp(int(data['etime'])).isoformat(' ')
    formatted_data['start'] = fromtimestamp(int(data['start'])).isoformat(' ')

    return formatted_data


def parse_logs(filename):
    """
    filename format YYYYMMDD
    """

    conn = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWD,
        db=DB_NAME)

    count = fail = skip = 0
    line_no = 0

    try:
        machine = get_machine(conn, MACHINE_NAME)
    except:
        print_error(
            filename, line_no,
            "Couldn't find machine named: %s" % MACHINE_NAME)
        sys.exit(1)

    # Try and open the log file
    try:
        f = open('%s%s' % (LOG_DIR, filename), 'r')
    except IOError:
        # print "Couldn't open file: %s" % '%s%s' % (LOG_DIR, filename)
        sys.exit(1)

    for line in f:
        line_no = line_no + 1
        try:
            data = pbs_to_dict(line)
        except ValueError:
            print_error(filename, line_no, "Wall time over 3 years")
        except:
            skip = skip + 1
            continue

        try:
            user_account = get_user_account(
                conn, data['user'], machine['category_id'])
        except:
            # Couldn't find user account - Assign to user 'Unknown_User'
            SQL = "SELECT * FROM user_account " \
                "WHERE username = 'unknown_user' " \
                "AND machine_category_id = '%s'" % machine['category_id']
            cursor = conn.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(SQL)
            rows = cursor.fetchall()
            cursor.close()
            user_account = rows[0]
            print_error(
                filename, line_no,
                "Couldn't find user account for "
                "username=%s and machine_category_id=%i"
                % (data['user'], machine['category_id']))
            fail = fail + 1

        # Get project id
        try:
            project_id = get_project(
                conn, data, user_account['default_project_id'])
        except:
            # Couldn't find project - Assign to 'Unknown_Project'
            if 'project' in data:
                print_error(
                    filename, line_no,
                    "Couldn't find project: %s" % data['project'])
            else:
                print_error(
                    filename, line_no,
                    "Couldn't find default project for "
                    "username=%s and machine_category_id=%i"
                    % (data['user'], machine['category_id']))
            project_id = 'Unknown_Project'
            fail = fail + 1

        # Everything is good so add entry
        username = data['user']
        user_id = int(user_account['id'])
        machine_id = int(machine['id'])
        date = datetime.date(
            int(filename[:4]), int(filename[4:6]), int(filename[6:]))
        # date = datetime.datetime.strptime(filename, '%Y%m%d')
        cpu_usage = data['cpu_usage']
        est_wall_time = data['est_wall_time']
        # undefined variable, se we make it up and keep PEP8 happy
        act_wall_time = 99

        queue = data['queue']
        mem = data['mem']
        vmem = data['vmem']
        ctime = data['ctime']
        qtime = data['qtime']
        etime = data['etime']
        start = data['start']

        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO cpu_job (user_id, project_id, machine_id, date, "
                "cpu_usage, queue_id, mem, vmem, ctime, qtime, etime, start, "
                "act_wall_time, est_wall_time, username) "
                "VALUES ('%i', '%s', '%i', '%s', '%i', '%s', '%i', '%i', "
                "'%s', '%s', '%s', '%s', '%i', '%i', '%s')"
                % (user_id, project_id, machine_id, date, cpu_usage,
                    queue, mem, vmem, ctime, qtime, etime, start,
                    act_wall_time, est_wall_time, username)
            )
            count = count + 1

            cursor.close()
            conn.commit()

        except:
            print_error(
                filename, line_no, "Failed to insert this line - %s" % data)
            fail = fail + 1
            continue

    conn.close()

    # print 'Inserted : %i' % count
    # print 'Failed   : %i' % fail
    # print 'Skiped   : %i' % skip


def read_all():
    """
    Reads all logs in directory
    used for initial import
    """
    import os

    file_list = os.listdir(LOG_DIR)

    for i in file_list:
        if not i == 'XML':
            parse_logs(i)


if __name__ == "__main__":

    if file_option:
        filename = opts['-f']
    else:
        # Get yesterdays date in a YYYYMMDD format
        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        filename = yesterday.strftime('%Y%m%d')

    parse_logs(filename)

    # read_all()
    sys.exit(0)
