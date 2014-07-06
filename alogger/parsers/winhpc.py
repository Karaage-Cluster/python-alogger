# Copyright 2008 VPAC
#
# This file is part of alogger-ng.
#
# alogger-ng is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# alogger-ng is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with alogger-ng  If not, see <http://www.gnu.org/licenses/>.


"""
Declare log parsing methods here.

methods take a line of a log and return a python dict containing

Key           | type     | Description
----------------------------------------------
user          | string   | username
project       | string   | pid
est_wall_time | int      | estimated wall time
act_wall_time | int      | actual wall time
cpu_usage     | int      | CPU usage in seconds
queue         | datetime | 
ctime         | datetime | 
qtime         | datetime | 
etime         | datetime |
start         | datetime |
jobid	      | string   |
cores	      | int      | number of cores
jobname       | string   | Job name
exit_status   | int      | Exit status

Optional
mem           | int      | memory used
vmem          | int      | virtual memory used
list_mem      | int      | memory requested
list_vmem     | int      | virtual memory requested
list_pmem     | int      | memory requested (per processor)
list_pvmem    | int      | virtual memory requested (per processor)

Raises value error if funky wall time

"""

import datetime
import logging

from alogger.utils import get_in_seconds, get_mem_in_kb, get_mem_in_mb


def winhpc_to_dict(line):
    """
    Parses a PBS log file line into a python dict
    
    raises KeyError when line not valid
    raises ValueError when time over 3 years

    """
    logging.debug('Parsing line:')
    logging.debug(line)
    # Split line into parts, only care about raw_data
    jobid, raw_data = line.split(' ', 1)
    
    data = {}
    formatted_data = {}
    
    formatted_data['jobid'] = jobid

    # Make into a dict using values key=value
    for d in raw_data.split(';'):
        try:
            key, value = d.split('=')
            data[key] = value
        except:
            continue
    print(jobid)
    print(data)
    # Check to see if line worth proccessing
    if 'REJMESSAGE' in data:
        return
    if 'COMPLETETIME' not in data:
        return
        #raise KeyError


    formatted_data['user'] = data['UNAME']
    if 'account' in data:
        formatted_data['project'] = data['']

    #formatted_data['jobname'] = data['jobname']
    formatted_data['group'] = data['GNAME']

    #formatted_data['ctime'] = datetime.datetime.fromtimestamp(int(data['ctime'])).isoformat(' ')
    start = datetime.datetime.fromtimestamp(int(data['STARTTIME']))
    end = datetime.datetime.fromtimestamp(int(data['COMPLETETIME']))
    formatted_data['qtime'] = datetime.datetime.fromtimestamp(int(data['QUEUETIME'])).isoformat(' ')
    formatted_data['etime'] = end.isoformat(' ')
    formatted_data['start'] = start.isoformat(' ')

    formatted_data['est_wall_time'] = data['WCLIMIT']
    formatted_data['act_wall_time'] = (end - start).seconds
 
    try:
        formatted_data['exec_hosts'] = data['HOSTLIST'].split(',')
    except:
        pass
    #cores = data['exec_host'].count('/')
    formatted_data['cores'] = int(data['TASKS'])
    formatted_data['cpu_usage'] = formatted_data['cores'] * formatted_data['act_wall_time']
    
    #formatted_data['queue'] = data['queue']
    
    formatted_data['exit_status'] = data['EXITCODE']
    #formatted_data['ctime'] = datetime.datetime.fromtimestamp(int(data['ctime'])).isoformat(' ')
    formatted_data['qtime'] = datetime.datetime.fromtimestamp(int(data['QUEUETIME'])).isoformat(' ')
    formatted_data['etime'] = datetime.datetime.fromtimestamp(int(data['COMPLETETIME'])).isoformat(' ')
    formatted_data['start'] = datetime.datetime.fromtimestamp(int(data['STARTTIME'])).isoformat(' ')

    logging.debug("Parsed following data")
    for k,v in formatted_data.items():
        logging.debug("%s = %s" % (k, v))
        
    return formatted_data

