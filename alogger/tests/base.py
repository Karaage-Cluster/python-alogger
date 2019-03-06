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
import filecmp
import json
import os.path
import shutil
import warnings

from .. import get_parser, log_to_dict
from . import examples, results


# disable rebuilding files
_testing_only = True

# force rebuilding files even if they exist
_force_rebuild = False


class Base(object):
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.maxDiff = None

    def test_line_to_dict(self):
        directory = os.path.abspath(os.path.split(examples.__file__)[0])
        path = os.path.join(directory, self.file_prefix+".log")
        with open(path, "r") as f:
            lines = f.readlines()

        parser = get_parser(self.log_type)

        directory = os.path.abspath(os.path.split(results.__file__)[0])
        path = os.path.join(directory, self.file_prefix+".json")
        if _testing_only or (os.path.isfile(path) and not _force_rebuild):

            with open(path, "r") as fp:
                expected_results = json.load(fp)

            for line in lines:
                expected_result = expected_results.pop(0)

                # depreciated
                try:
                    with warnings.catch_warnings(record=True):
                        warnings.simplefilter("always")
                        result = log_to_dict(line, self.log_type)
                    self.assertIsNotNone(result)
                except KeyError:
                    result = None
                self.assertEqual(result, expected_result)

                # current
                result = parser.line_to_dict(line)
                self.assertEqual(result, expected_result)

        else:
            test_results = []

            for line in lines:
                # depreciated
                try:
                    with warnings.catch_warnings(record=True):
                        warnings.simplefilter("always")
                        result1 = log_to_dict(line, self.log_type)
                    self.assertIsNotNone(result1)
                except KeyError:
                    result1 = None

                # current
                result2 = parser.line_to_dict(line)

                # compare depreciated with current
                self.assertEqual(result1, result2)

                # save result
                test_results.append(result1)

            with open(path, "w") as fp:
                json.dump(test_results, fp, sort_keys=True, indent=4)

    def get_cfg(self):
        directory = os.path.abspath(os.path.split(examples.__file__)[0])
        return {
            'log_dir': directory,
            'log_filename': self.file_prefix+".log",
        }

    def test_read_log(self):
        directory = os.path.abspath(os.path.split(examples.__file__)[0])
        expected_text_path = os.path.join(directory, self.file_prefix+".log")

        tmp_dir = "tmp"
        if not os.path.isdir(tmp_dir):
            os.mkdir(tmp_dir)

        date = datetime.date.today()

        cfg = self.get_cfg()
        cfg.update({
            'text_dir': tmp_dir,
        })

        text_filename = date.strftime('%Y%m%d')
        text_path = os.path.join(tmp_dir, text_filename)

        parser = get_parser(self.log_type)

        directory = os.path.abspath(os.path.split(results.__file__)[0])
        path = os.path.join(directory, self.file_prefix+".json")
        if _testing_only or (os.path.isfile(path) and not _force_rebuild):

            with open(path, "r") as fp:
                expected_results = json.load(fp)

            for result in parser.read_log(date, cfg):
                expected_result = expected_results.pop(0)
                self.assertEqual(result, expected_result)

            self.assertTrue(filecmp.cmp(text_path, expected_text_path))

        else:
            test_results = []

            for result in parser.read_log(date, cfg):
                test_results.append(result)

            with open(path, "w") as fp:
                json.dump(test_results, fp, sort_keys=True, indent=4)

            shutil.copyfile(text_path, expected_text_path)
