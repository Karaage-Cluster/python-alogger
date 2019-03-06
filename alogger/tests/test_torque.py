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

import unittest
import warnings

from .base import Base


class TestTorque(Base, unittest.TestCase):
    file_prefix = "torque"
    log_type = "TORQUE"


class TestPBS(Base, unittest.TestCase):
    file_prefix = "torque"
    log_type = "PBS"
    # legacy

    def test_line_to_dict(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            super(TestPBS, self).test_line_to_dict()
            self.assertTrue(len(w) == 1)
            self.assertTrue(
                issubclass(w[0].category, DeprecationWarning))

    def test_read_log(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            super(TestPBS, self).test_read_log()
            self.assertTrue(len(w) == 1)
            self.assertTrue(
                issubclass(w[0].category, DeprecationWarning))
