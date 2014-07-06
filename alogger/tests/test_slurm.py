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

import unittest
from alogger import log_to_dict
import os.path


class TestSlurm(unittest.TestCase):

    def test_log_to_dict(self):
        directory = os.path.abspath(os.path.split(__file__)[0])
        fd = open(os.path.join(directory, 'examples/slurm'))
        lines = fd.readlines()
        fd.close()

        for line in lines:
            log_to_dict(line, 'slurm')
