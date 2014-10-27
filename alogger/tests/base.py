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

from alogger import log_to_dict, Parser
import os.path
import json
import warnings


# disable rebuilding files
_testing_only = True

# force rebuilding files even if they exist
_force_rebuild = False


class Base(object):

    def test_log_to_dict(self):
        directory = os.path.abspath(os.path.split(__file__)[0])
        path = os.path.join(directory, 'examples', self.file_prefix+".log")
        fd = open(path, "r")
        lines = fd.readlines()
        fd.close()

        parser = Parser(self.log_type)

        path = os.path.join(directory, 'results', self.file_prefix+".json")
        if _testing_only or (os.path.isfile(path) and not _force_rebuild):

            with open(path, "r") as fp:
                expected_results = json.load(fp)

            for line in lines:
                expected_result = expected_results.pop(0)

                # depreciated
                try:
                    with warnings.catch_warnings(record=True) as w:
                        warnings.simplefilter("always")
                        result = log_to_dict(line, self.log_type)
                        self.assertEqual(len(w), 1)
                        self.assertTrue(
                            issubclass(w[0].category, DeprecationWarning))
                    self.assertIsNotNone(result)
                except KeyError:
                    result = None
                self.assertEqual(result, expected_result)

                # current
                result = parser.log_to_dict(line)
                self.assertEqual(result, expected_result)

        else:
            results = []

            for line in lines:
                try:
                    with warnings.catch_warnings(record=True) as w:
                        warnings.simplefilter("always")
                        result1 = log_to_dict(line, self.log_type)
                        self.assertEqual(len(w), 1)
                        self.assertTrue(
                            issubclass(w[0].category, DeprecationWarning))
                    self.assertIsNotNone(result1)
                except KeyError:
                    result1 = None
                result2 = parser.log_to_dict(line)
                self.assertEqual(result1, result2)

                results.append(result1)

            with open(path, "w") as fp:
                json.dump(results, fp, indent=4)
