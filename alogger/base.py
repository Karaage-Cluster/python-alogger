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
from __future__ import absolute_import, print_function, unicode_literals

import errno
import logging
import os.path


logger = logging.getLogger(__name__)

_plugins = {}


class TextLog(object):
    def __init__(self, date, cfg):
        if 'text_dir' in cfg:
            text_dir = cfg['text_dir']

            filename = date.strftime('%Y%m%d')
            path = os.path.join(text_dir, filename)
            self._f = open(path, 'w')
        else:
            self._f = None

    def line(self, line):
        if self._f is not None:
            if line[-1] == "\n":
                line = line[0:-1]
            print(line, file=self._f)

    def close(self):
        if self._f is not None:
            self._f.close()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()


class BaseParser(object):

    def read_log(self, date, cfg):
        filename = date.strftime('%Y%m%d')
        filename = cfg.get('log_filename', filename)

        path = os.path.join(cfg['log_dir'], filename)

        try:
            with open(path, 'r') as f:
                with TextLog(date, cfg) as log:
                    for line in f:
                        log.line(line)
                        yield self.line_to_dict(line, cfg)
        except IOError as ex:
            if ex.errno == errno.ENOENT:
                pass  # ignore file not found error
            else:
                raise

    def line_to_dict(self, line, cfg=None):
        raise NotImplementedError()
