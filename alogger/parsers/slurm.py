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
from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import time
import logging
logger = logging.getLogger(__name__)


def slurm_suffix_to_megabytes(memory_string):

    return slurm_suffix(memory_string) / 1024 / 1024


def slurm_suffix_to_kilobytes(memory_string):

    return slurm_suffix(memory_string) / 1024


def slurm_suffix(memory_string):

    if memory_string.endswith('K'):
        return int(float(memory_string[:-1]) * 1024)
    elif memory_string.endswith('M'):
        return int(float(memory_string[:-1]) * 1024 * 1024)
    elif memory_string.endswith('G'):
        return int(float(memory_string[:-1]) * 1024 * 1024 * 1024)
    elif memory_string.endswith('T'):
        return int(float(memory_string[:-1]) * 1024 * 1024 * 1024 * 1024)
    else:
        return int(memory_string)


#  Maybe there is some isomething in datetime that takes a ISO std string but I
#  cannot find it, DRB.
def DateTime_from_String(datetimeSt):
    """Gets a date time string like 2010-09-10T15:54:18 and retuns a datetime
    object raises a ValueError if it all goes wrong """
    DayTime = datetimeSt.split('T')
    if len(DayTime) != 2:
        raise ValueError

    Date = DayTime[0].split('-')
    if len(Date) != 3:
        raise ValueError

    Time = DayTime[1].split(':')
    if len(Time) != 3:
        raise ValueError

    dt = datetime.datetime(
        year=int(Date[0]),
        month=int(Date[1]),
        day=int(Date[2]),
        hour=int(Time[0]),
        minute=int(Time[1]),
        second=int(Time[2])
    )
    return dt


def SecondsFromSlurmTime(timeString):
    """This function could be merged into get_in_seconds above but its here to
    leave clear break between the Slurm addition and original.  It deals with
    the fact that slurm may return est_wall_time as 00nnn, 00:00:00 or
    0-00:00:00.  """
    if timeString.find(':') == -1:              # straight second format
        return int(timeString)
    if timeString.find('-') == -1:              # must be a (eg) 10:00:00 case
        Seconds = (
            (int(timeString.split(':')[0]) * 3600)
            + ((int(timeString.split(':')[1]) * 60))
            + int(timeString.split(':')[2])
        )
    else:
        DayRest = timeString.split('-')
        Seconds = int(DayRest[0]) * 3600 * 24
        Seconds = Seconds + (int(DayRest[1].split(':')[0]) * 3600)
        Seconds = Seconds + ((int(DayRest[1].split(':')[1]) * 60))
        Seconds = Seconds + int(DayRest[1].split(':')[2])
    return Seconds


def line_to_dict(line):
    """Parses a Slurm log file into dictionary"""
    raw_data = line.split(' ')
    data = {}
    formatted_data = {}
    # break up line into a temp dictionary
    last_key = False
    for d in raw_data:
        try:
            key, value = d.split('=')
            data[key] = value
            last_key = key
        except ValueError:
            if last_key:
                data[last_key] = "%s %s" % (data[last_key], d)
            continue

    # Note that the order these are done in is important !
    formatted_data['jobid'] = data['JobId']
    formatted_data['cores'] = int(data['ProcCnt'])

    # 'mike(543)' - remove the uid in brackets.
    formatted_data['user'] = data['UserId'][:data['UserId'].find('(')]
    formatted_data['project'] = data['Account']

    # If SubmitTime is invalid and non-existant use StartTime instead.
    try:
        # '2010-07-30T15:34:39'
        formatted_data['qtime'] = \
            DateTime_from_String(data['SubmitTime']).isoformat(str(' '))
        # for practical purposes, same as etime here.
        formatted_data['ctime'] = \
            DateTime_from_String(data['SubmitTime']).isoformat(str(' '))
    except (ValueError, KeyError):
        # old records don't have a submit time time.
        formatted_data['qtime'] = \
            DateTime_from_String(data['StartTime']).isoformat(str(' '))
        formatted_data['ctime'] = \
            DateTime_from_String(data['StartTime']).isoformat(str(' '))

    # If data['StartTime'] or data['EndTime'] is bad or not given, the
    # following statements will fail
    formatted_data['start'] = \
        DateTime_from_String(data['StartTime']).isoformat(str(' '))
    # formatted_data['etime']  # don't care
    formatted_data['act_wall_time'] = \
        int(time.mktime(DateTime_from_String(data['EndTime']).timetuple())) \
        - int(time.mktime(DateTime_from_String(data['StartTime']).timetuple()))
    formatted_data['record_time'] = \
        DateTime_from_String(data['StartTime']).isoformat(str(' '))
    formatted_data['cpu_usage'] = \
        formatted_data['act_wall_time'] * formatted_data['cores']

    # Note that this is the name of the script, not --jobname
    formatted_data['jobname'] = data['Name']
    try:
        # might be 5-00:00:00 or 18:00:00
        formatted_data['est_wall_time'] = \
            SecondsFromSlurmTime(data['TimeLimit'])
    except ValueError:
        # Sometimes returns 'UNLIMITED' !
        formatted_data['est_wall_time'] = -1
    try:
        # might be "COMPLETED", "CANCELLED", "TIMEOUT" and may have multiple
        # entries per line !
        formatted_data['exit_status'] = int(data['JobState'])
    except ValueError:
        # Watch out, Sam says dbase expects an int !!!
        formatted_data['exit_status'] = 0

    formatted_data['queue'] = data['Partition']
    formatted_data['vmem'] = 0
    if 'MinMemoryCPU' in data:
        formatted_data['list_pmem'] = \
            slurm_suffix_to_megabytes(data['MinMemoryCPU'])
    else:
        formatted_data['list_pmem'] = 0

    if 'MinMemoryNode' in data:
        formatted_data['list_mem'] = \
            slurm_suffix_to_megabytes(data['MinMemoryNode'])
    else:
        formatted_data['list_mem'] = 0

    if 'ReqMem' in data:
        if data['ReqMem'].endswith('c'):
            formatted_data['list_pmem'] = \
                slurm_suffix_to_megabytes(data['ReqMem'][:-1])
        elif data['ReqMem'].endswith('n'):
            formatted_data['list_mem'] = \
                slurm_suffix_to_megabytes(data['ReqMem'][:-1])
        else:
            logger.error("Weird formatting of ReqMem")

    if 'MaxVMSize' in data:
        formatted_data['mem'] = slurm_suffix_to_kilobytes(data['MaxVMSize'])
    else:
        formatted_data['mem'] = 0
    formatted_data['list_vmem'] = 0
    formatted_data['list_pvmem'] = 0
    formatted_data['etime'] = formatted_data['qtime']
    # Things we don't seem to have available, would like qtime and
    # est_wall_time mem, qtime, list_pmem, list_pvmem, queue, vmem, list_vmem,
    # jobname.  Note that "out of the box" slurm does not report on Queue or
    # Creation time.
    return formatted_data
