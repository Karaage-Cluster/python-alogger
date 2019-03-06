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


"""
Declare log parsing methods in here.
methods take a line of a log and return a python dict containing
Key           | type     | Description
----------------------------------------------
user          | string   | username
project       | string   | pid
est_wall_time | int      | estimated wall time
act_wall_time | int      | actual wall time
cpu_usage     | int      | CPU usage in seconds
queue         | datetime |
ctime         | datetime | the time in seconds when the job
              |          | was Created (first submitted)
qtime         | datetime | the time in seconds when the job
              |          | was Queued into the current queue
etime         | datetime | time in seconds when the job became Eligible to run
start         | datetime | the time in seconds when job execution Started
jobid         | string   | Expected to also have host name
cores         | int      | number of cores
jobname       | string   | Job name
exit_status   | int      | Exit status - or a string from Slurm !
Optional
mem           | int      | memory used
vmem          | int      | virtual memory used
list_mem      | int      | memory requested
list_vmem     | int      | virtual memory requested
list_pmem     | int      | memory requested (per processor)
list_pvmem    | int      | virtual memory requested (per processor)
Raises value error if funky wall time

So a user submits a job, thats "qtime" (or, probably 'ctime')
eventually, its starts to run, that "start"
finally, it finishes, one way or another, thats "start" + "act_wall_time"

If queue is light, etime can equal qtime, but not if the job is blocked.

"""
