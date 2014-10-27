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

import importlib
import warnings
import logging
logger = logging.getLogger(__name__)

_plugins = {}


def register_plugin(module_name, log_type):
    _plugins[log_type] = module_name

register_plugin("alogger.parsers.torque", "PBS")
register_plugin("alogger.parsers.sge", "SGE")
register_plugin("alogger.parsers.slurm", "SLURM")
register_plugin("alogger.parsers.winhpc", "WINHPC")


class InvalidLogType(Exception):
    pass


def _get_line_to_dict(log_type):
    try:
        module_name = _plugins[log_type]
    except KeyError:
        logger.error('Cannot find parser for log type: %s' % log_type)
        raise InvalidLogType('Cannot find parser for log type: %s' % log_type)

    module = importlib.import_module(module_name)

    try:
        line_to_dict = module.line_to_dict
    except AttributeError:
        logger.error('Invalid parser for log type: %s' % log_type)
        raise InvalidLogType('Invalid parser for log type: %s' % log_type)

    return line_to_dict


def log_to_dict(line, log_type):
    warnings.warn('log_to_dict depreciated', DeprecationWarning)

    line_to_dict = _get_line_to_dict(log_type)
    result = line_to_dict(line)

    # required for backwards compatability
    if result is None:
        raise KeyError

    return result


class Parser(object):

    def __init__(self, log_type):
        self._log_type = log_type
        self._line_to_dict = _get_line_to_dict(log_type)

    def log_to_dict(self, line):
        return self._line_to_dict(line)
