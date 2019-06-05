#!/usr/bin/env python

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

import sys

from setuptools import Command, setup, find_packages


VERSION='2.2.12'

class VerifyVersionCommand(Command):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'
    user_options = [
      ('version=', None, 'expected version'),
    ]

    def initialize_options(self):
        self.version = None

    def finalize_options(self):
        pass

    def run(self):
        version = self.version

        if version != VERSION:
            info = "{0} does not match the version of this app: {1}".format(
                version, VERSION
            )
            sys.exit(info)

setup(
    name="python-alogger",
    version=VERSION,
    url='https://github.com/Karaage-Cluster/python-alogger',
    author='Brian May',
    author_email='brian@linuxpenguins.xyz',
    description='Small python library to parse resource manager logs',
    packages=find_packages(),
    license="GPL3+",
    long_description=open('README.rst').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 "
        "or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="karaage cluster user administration",
    package_data={
        '': ['*.log', '*.json'],
    },
    tests_require=[
        "pytest",
        "pytest-runner",
    ],
    cmdclass={
        'verify': VerifyVersionCommand,
    }
)
