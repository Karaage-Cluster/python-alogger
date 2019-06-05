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

import importlib
import logging
import warnings


logger = logging.getLogger(__name__)


__author__ = """Brian May"""
__email__ = 'brian@linuxpenguins.xyz'
__version__ = '2.2.12'

_plugins = {}


def register_plugin(module_name, log_type):
    _plugins[log_type] = module_name


register_plugin("alogger.parsers.torque.Parser", "TORQUE")
register_plugin("alogger.parsers.torque.PbsParser", "PBS")
register_plugin("alogger.parsers.sge.Parser", "SGE")
register_plugin("alogger.parsers.slurm.Parser", "SLURM")
register_plugin("alogger.parsers.winhpc.Parser", "WINHPC")


class InvalidLogType(Exception):
    pass


def get_parser(log_type):
    try:
        module_name, _, name = _plugins[log_type].rpartition(".")
    except KeyError:
        logger.error('Cannot find parser for log type: %s' % log_type)
        raise InvalidLogType('Cannot find parser for log type: %s' % log_type)

    module = importlib.import_module(module_name)
    cls = getattr(module, name)

    parser = cls()
    return parser


def log_to_dict(line, log_type):
    warnings.warn('log_to_dict depreciated', DeprecationWarning)

    parser = get_parser(log_type)
    result = parser.line_to_dict(line)

    # required for backwards compatability
    if result is None:
        raise KeyError

    return result
