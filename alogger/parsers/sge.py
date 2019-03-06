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

import datetime
import logging

from ..base import BaseParser


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

logger = logging.getLogger(__name__)


class Parser(BaseParser):

    def line_to_dict(self, line, cfg=None):
        """
        Parses a SGE accounting log file line into a python dict

        raises ValueError when line not valid

        """
        try:
            queue, hostname, group, username, jobname, jobid, account, \
                priority, \
                qsub_time, start_time, end_time, failed, exit_status, \
                ru_wallclock, ru_utime, ru_stime, ru_maxrss, ru_ixrss, \
                ru_ismrss, ru_idrss,  ru_isrss, ru_minflt, ru_majflt, \
                ru_nswap, ru_inblock, ru_oublock, ru_msgsnd, ru_msgrcv, \
                ru_nsignals, ru_nvcsw, ru_nivcsw, project, department, \
                granted_pe, slots, UNKNOWN, cpu, mem, UNKNOWN, \
                command_line_arguments, UNKNOWN, UNKNOWN, \
                maxvmem_bytes = line.split(':')
        except ValueError:
            a1, a2, queue, hostname, group, username, jobname, jobid, \
                account, \
                priority, qsub_time, start_time, end_time, failed, \
                exit_status, \
                ru_wallclock, ru_utime, ru_stime, ru_maxrss, ru_ixrss, \
                ru_ismrss, \
                ru_idrss,  ru_isrss, ru_minflt, ru_majflt, ru_nswap, \
                ru_inblock, \
                ru_oublock, ru_msgsnd, ru_msgrcv, ru_nsignals, ru_nvcsw, \
                ru_nivcsw, project, department, granted_pe, slots, UNKNOWN, \
                cpu, mem, UNKNOWN, command_line_arguments, UNKNOWN, UNKNOWN, \
                maxvmem_bytes = line.split(':')

        formatted_data = {}

        formatted_data['jobid'] = jobid

        formatted_data['date'] = \
            datetime.datetime.fromtimestamp(int(end_time)).isoformat(str(' '))
        formatted_data['user'] = username

        formatted_data['jobname'] = jobname
        try:
            formatted_data['est_wall_time'] = None
            formatted_data['act_wall_time'] = int(ru_wallclock)
        except ValueError:
            logger.error(
                'Failed to parse act_wall_time value: %s' % ru_wallclock)
            raise ValueError

        formatted_data['cores'] = int(slots)
        formatted_data['cpu_usage'] = \
            formatted_data['cores'] * formatted_data['act_wall_time']

        formatted_data['queue'] = queue

        formatted_data['start'] = \
            datetime.datetime.fromtimestamp(int(qsub_time)).isoformat(str(' '))
        formatted_data['exit_status'] = exit_status

        logger.debug("Parsed following data")
        for k, v in formatted_data.items():
            logger.debug("%s = %s" % (k, v))

        return formatted_data
