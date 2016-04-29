#!/usr/bin/env python

# Copyright 2007-2014 VPAC
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

from setuptools import setup, find_packages

setup(
    name="python-alogger",
    use_scm_version={
        'write_to': "alogger/version.py",
    },
    setup_requires=['setuptools_scm'],
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
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="karaage cluster user administration",
    package_data={
        '': ['*.log', '*.json'],
    },
    test_suite="alogger.tests",
)
