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

def log_to_dict(line, LOG_TYPE):

    if LOG_TYPE == 'PBS':
        from alogger.parsers.torque import pbs_to_dict as line_to_dict

    elif LOG_TYPE == 'SGE':
        from alogger.parsers.sge import sge_to_dict as line_to_dict
    elif LOG_TYPE == 'SLURM':
        from alogger.parsers.slurm import slurm_to_dict as line_to_dict
    elif LOG_TYPE == 'WINHPC':
        from alogger.parsers.winhpc import winhpc_to_dict as line_to_dict
    else:
        logging.error('Cannot find parser for log type: %s' % LOG_TYPE)
        raise KeyError

    return line_to_dict(line)
