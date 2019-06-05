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

import logging
import re


"""
python-alogger utils

"""

logger = logging.getLogger(__name__)


def print_error(line_no, message):
    """
    Method called when error occurs
    """
    print('Line: %s --- %s' % (line_no, message))


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


def get_mem_in_kb(memory_string):
    # Strip kb or b etc. from end of mem entries
    # Example imput 304kb or 322b
    mem_re = re.compile('([0-9]*)([a-zA-Z]*)')
    memory, unit = mem_re.match(memory_string).groups()
    memory = int(memory)
    if unit == 'kb':
        return memory
    elif unit == 'b':
        return memory / 1024
    elif unit == 'mb':
        return memory * 1024
    elif unit == 'gb':
        return memory * 1024 * 1024
    elif unit == 'tb':
        return memory * 1024 * 1024 * 1024
    else:
        logger.error('Failed to parse memory value: %s' % memory_string)
        raise ValueError


def get_mem_in_mb(memory_string):
    return get_mem_in_kb(memory_string) / 1024
