# Copyright 2013-2017, Brian May
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
from __future__ import absolute_import, unicode_literals

import csv
import datetime
import logging
import subprocess
import sys
import time

from ..base import BaseParser, TextLog


logger = logging.getLogger(__name__)


if sys.version_info < (3, 0):
    # Python2: csv module does not support unicode, we must use byte strings.

    def _input_csv(csv_data):
        for line in csv_data:
            assert isinstance(line, bytes)
            yield line

    def _output_csv(csv_line):
        for i, column in enumerate(csv_line):
            csv_line[i] = column.decode("ascii", errors='ignore')
            assert isinstance(csv_line[i], unicode)  # NOQA

else:
    # Python3: csv module does support unicode, we must use strings everywhere,
    # not byte strings

    def _input_csv(unicode_csv_data):
        for line in unicode_csv_data:
            assert isinstance(line, bytes)
            line = line.decode("ascii", errors='ignore')
            assert isinstance(line, str)
            yield line

    def _output_csv(csv_line):
        for column in csv_line:
            assert isinstance(column, str)


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


class Parser(BaseParser):

    def read_log(self, date, cfg):
        date_from = date
        date_to = date + datetime.timedelta(days=1)

        cmd = []
        cmd.append(cfg['sacct_path'])
        cmd.extend([
            '-o', 'Cluster,JobID,User,UID,Group,GID,Account,JobName,'
            'State,Partition,Timelimit,Elapsed,Start,End,Submit,Eligible,'
            'AllocCPUS,NodeList,ReqMem'])
        cmd.extend(['-p', '-X', '-s', 'CA,CD,F,NF,TO'])
        cmd.append('--starttime='+date_from.strftime('%Y%m%d'))
        cmd.append('--endtime='+date_to.strftime('%Y%m%d'))

        command = cmd

        logger.debug("Cmd %s" % command)
        with open('/dev/null', 'w') as null:
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=null)

        reader = csv.reader(_input_csv(process.stdout), delimiter=str("|"))

        try:
            headers = next(reader)
            logger.debug("<-- headers %s" % headers)
        except StopIteration:
            logger.debug("Cmd %s headers not found" % command)
            headers = []

        with TextLog(date, cfg) as log:
            for row in reader:
                _output_csv(row)

                logger.debug("<-- row %s" % row)
                this_row = {}

                i = 0
                for i in range(0, len(headers)):
                    key = headers[i]
                    value = row[i]
                    this_row[key] = value

                JobID = "%s.%s%s" % (
                    this_row['JobID'], this_row['Cluster'],
                    cfg.get("jobid_postfix", ""))

                AllocCPUS = int(this_row['AllocCPUS'])
                State = this_row['State'].split(" ")

                if AllocCPUS > 0:
                    results = []
                    results.append("JobId=%s" % JobID)
                    results.append("UserId=%s(%s)"
                                   % (this_row['User'], this_row['UID']))
                    results.append("GroupId=%s(%s)"
                                   % (this_row['Group'], this_row['GID']))
                    results.append("Account=%s" % (this_row['Account']))
                    results.append("Name=%s" % (this_row['JobName']))
                    results.append("JobState=%s" % (State[0]))
                    results.append("Partition=%s" % (this_row['Partition']))
                    results.append("TimeLimit=%s" % (this_row['Timelimit']))
                    results.append("RunTime=%s" % (this_row['Elapsed']))
                    results.append("StartTime=%s" % (this_row['Start']))
                    results.append("EndTime=%s" % (this_row['End']))
                    results.append("SubmitTime=%s" % (this_row['Submit']))
                    results.append("EligibleTime=%s" % (this_row['Eligible']))
                    results.append("ProcCnt=%s" % (this_row['AllocCPUS']))
                    results.append("NodeList=%s" % (this_row['NodeList']))

                    if this_row['ReqMem'][-1] == 'n':
                        results.append(
                            "MinMemoryNode=%s" % (this_row['ReqMem'][0:-1]))
                    elif this_row['ReqMem'][-1] == 'c':
                        results.append(
                            "MinMemoryCPU=%s" % (this_row['ReqMem'][0:-1]))

                    line = " ".join(results)
                    log.line(line)
                    yield self.line_to_dict(line)

        process.stdout.close()
        retcode = process.wait()
        if retcode != 0:
            logger.error("<-- Cmd %s returned %d (error)" % (command, retcode))
            raise subprocess.CalledProcessError(retcode, command)

        if len(headers) == 0:
            logger.error("Cmd %s didn't return any headers." % command)
            raise RuntimeError("Cmd %s didn't return any headers." % command)

        logger.debug("<-- Returned: %d (good)" % (retcode))

    def line_to_dict(self, line):
        """Parses a Slurm log file into dictionary"""
        raw_data = line.strip().split(' ')
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

        start_time = DateTime_from_String(data['StartTime'])
        end_time = DateTime_from_String(data['EndTime'])

        # If SubmitTime is invalid and non-existant use StartTime instead.
        try:
            # '2010-07-30T15:34:39'
            submit_time = DateTime_from_String(data['SubmitTime'])
        except (ValueError, KeyError):
            submit_time = start_time

        # '2010-07-30T15:34:39'
        formatted_data['qtime'] = submit_time.isoformat(str(' '))
        # for practical purposes, same as etime here.
        formatted_data['ctime'] = submit_time.isoformat(str(' '))

        # If data['StartTime'] or data['EndTime'] is bad or not given, the
        # following statements will fail
        formatted_data['start'] = start_time.isoformat(str(' '))
        # formatted_data['etime']  # don't care
        formatted_data['act_wall_time'] = \
            int(time.mktime(end_time.timetuple())) \
            - int(time.mktime(start_time.timetuple()))
        formatted_data['record_time'] = start_time.isoformat(str(' '))
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
            # might be "COMPLETED", "CANCELLED", "TIMEOUT" and may have
            # multiple entries per line !
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
            formatted_data['mem'] = \
                slurm_suffix_to_kilobytes(data['MaxVMSize'])
        else:
            formatted_data['mem'] = 0
        formatted_data['list_vmem'] = 0
        formatted_data['list_pvmem'] = 0
        formatted_data['etime'] = formatted_data['qtime']
        # Things we don't seem to have available, would like qtime and
        # est_wall_time mem, qtime, list_pmem, list_pvmem, queue, vmem,
        # list_vmem, jobname.  Note that "out of the box" slurm does not report
        # on Queue or Creation time.
        return formatted_data
