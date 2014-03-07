#!/usr/bin/env python

# Copyright 2008-2014 VPAC
#
# This file is part of django-tldap.
#
# django-tldap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-tldap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with django-tldap  If not, see <http://www.gnu.org/licenses/>.
from setuptools import setup, find_packages
import os

with open('VERSION.txt', 'r') as f:
    version = f.readline().strip()

setup(
    name = "python-alogger",
    version = version,
    url = 'https://github.com/Karaage-Cluster/python-alogger',
    author = 'Brian May',
    author_email = 'brian@vpac.org',
    description = 'Small python library to parse resource manager logs',
    packages = find_packages(),
    license = "GPL3+",
    long_description = open('README.rst').read(),
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords = "karaage cluster user administration",
)
