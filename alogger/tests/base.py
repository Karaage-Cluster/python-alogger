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

from alogger import log_to_dict
import os.path
import json

_testing_only = True


class Base(object):

    def test_log_to_dict(self):
        directory = os.path.abspath(os.path.split(__file__)[0])
        path = os.path.join(directory, 'examples', self.file_prefix+".log")
        fd = open(path, "r")
        lines = fd.readlines()
        fd.close()

        path = os.path.join(directory, 'results', self.file_prefix+".json")
        if _testing_only or os.path.isfile(path):

            with open(path, "r") as fp:
                expected_results = json.load(fp)

            for line in lines:
                result = log_to_dict(line, self.log_type)
                expected_result = expected_results.pop(0)
                self.assertEqual(result, expected_result)

        else:
            results = []

            for line in lines:
                results.append(log_to_dict(line, self.log_type))

            with open(path, "w") as fp:
                json.dump(results, fp, indent=4)
