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
import warnings

from alogger.utils import get_in_seconds, get_mem_in_kb, get_mem_in_mb

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
jobid         | string   |
cores         | int      | number of cores
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
        Parses a PBS log file line into a python dict

        raises ValueError when line not valid

        """
        if cfg is None:
            cfg = {}

        logger.debug('Parsing line:')
        logger.debug(line)
        # Split line into parts, only care about raw_data
        date, random, job_num, raw_data = line.split(';')

        raw_data = raw_data.split(str(' '))

        data = {}
        formatted_data = {}

        formatted_data['jobid'] = job_num

        # Make into a dict using values key=value
        for d in raw_data:
            try:
                key, value = d.split('=')
                data[key] = value
            except ValueError:
                continue

        # Check to see if line worth proccessing
        if 'resources_used.walltime' not in data:
            return None

        formatted_data['user'] = data['user']
        formatted_data['project'] = None
        if 'project' in data:
            formatted_data['project'] = data['project']
        elif 'account' in data:
            formatted_data['project'] = data['account']

        ignore_project = cfg.get('ignore_project', None)
        if ignore_project is not None \
                and formatted_data['project'] == ignore_project:
            formatted_data['project'] = None

        if formatted_data['project'] is None:
            formatted_data['project'] = cfg.get('default_project', None)

        formatted_data['jobname'] = data['jobname']
        formatted_data['group'] = data['group']

        formatted_data['act_wall_time'] = \
            get_in_seconds(data['resources_used.walltime'])

        if 'Resource_List.walltime' in data:
            formatted_data['est_wall_time'] = \
                get_in_seconds(data.get('Resource_List.walltime'))
        else:
            formatted_data['est_wall_time'] = None

        formatted_data['exec_hosts'] = \
            [x[:-2] for x in data['exec_host'].split('+')]

        if 'resources_used.ncpus' in data:
            cores = int(data['resources_used.ncpus'])
        else:
            cores = data['exec_host'].count('/')
        formatted_data['cores'] = cores
        formatted_data['cpu_usage'] = cores * formatted_data['act_wall_time']

        formatted_data['queue'] = data['queue']

        formatted_data['mem'] = \
            get_mem_in_kb(data.get('resources_used.mem', '0kb'))
        formatted_data['vmem'] = \
            get_mem_in_kb(data.get('resources_used.vmem', '0kb'))

        formatted_data['list_pmem'] = \
            get_mem_in_mb(data.get('Resource_List.pmem', '0kb'))
        formatted_data['list_mem'] = \
            get_mem_in_mb(data.get('Resource_List.mem', '0kb'))

        formatted_data['list_vmem'] = \
            get_mem_in_mb(data.get('Resource_List.vmem', '0kb'))
        formatted_data['list_pvmem'] = \
            get_mem_in_mb(data.get('Resource_List.pvmem', '0kb'))

        formatted_data['exit_status'] = data['Exit_status']

        fromtimestamp = datetime.datetime.fromtimestamp
        formatted_data['ctime'] = \
            fromtimestamp(int(data['ctime'])).isoformat(str(' '))
        formatted_data['qtime'] = \
            fromtimestamp(int(data['qtime'])).isoformat(str(' '))
        formatted_data['etime'] = \
            fromtimestamp(int(data['etime'])).isoformat(str(' '))
        formatted_data['start'] = \
            fromtimestamp(int(data['start'])).isoformat(str(' '))

        logger.debug("Parsed following data")
        for k, v in formatted_data.items():
            logger.debug("%s = %s" % (k, v))

        return formatted_data


class PbsParser(Parser):
    def __init__(self):
        warnings.warn(
            'PBS parser obsolete; use TORQUE instead.', DeprecationWarning)
        super(PbsParser, self).__init__()
