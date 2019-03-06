==========
Change log
==========
All notable changes to this project will be documented in this file. The format
is based on `Keep a Changelog`_ and this project
adheres to `Semantic Versioning`_.

.. _`Keep a Changelog`: http://keepachangelog.com/
.. _`Semantic Versioning`: http://semver.org/


2.2.11 - 2018-03-06
-------------------

Changes
~~~~~~~
* Use circleci for builds


2.2.10 - 2017-05-20
-------------------

Fixed
~~~~~
* Various minor issues with tests.
* Incorrect copyright notices, referring to VPAC which no longer exists.


2.2.9 - 2016-05-03
------------------

* Update my email address.


2.2.8 - 2016-04-29
------------------

* Fix problems in MANIFEST.in


2.2.7 - 2016-04-29
------------------

* Split out Debian packaging
* Fix flake8 issues.


2.2.6 - 2015-04-20
------------------

* torque: Fix est_wall_time.
* torque (PBS Pro): Fix core count.


2.2.5 - 2015-03-31
------------------

* New config options to allow replacing default project.


2.2.4 - 2015-03-06
------------------

* PBS Pro uses 'project' not 'account'.
* Simplify act_wall_time processing.
* est_wall_time is optional and can be None.


2.2.3 - 2014-10-31
------------------

* Support PBS parser as legacy alias for TORQUE.
* Ignore file not found error when reading TORQUE log file.
* Fix RPM package version.


2.2.2 - 2014-10-30
------------------

* Include test data.
* New API to read from source. Note: Slurm reader still incomplete, memory
  usage information will not be read.
* Update sample torque log file.


2.2.1 - 2014-10-27
------------------

* New version.
* More tests.


2.2.0 - 2014-07-07
------------------

* Add Vcs headers.
* Python3 package.
* New release.
* Fix print syntax for Python3.
* Fix PEP8 issues and tests.
* Fix copyright notices.
* Check the results of the tests.
* git ignore file.
* Update pypi classifiers, we have Python3 support.
* Add missing file.
* Fix comments.
* New plugin architecture.


2.1.7 - 2014-05-19
------------------

* Updates for Slurm support. Contributed by VLSCI.


2.1.6 - 2014-03-11
------------------

* Update python packaging.
* Update information.
* No functional changes.


2.1.5 - 2014-01-29
------------------

* Update Debian packaging.


2.1.4 - 2013-05-28
------------------

* Update Debian packaging.
* Slurm specific changes from 2010.
* Initial attempt for Windows HPC support from 2011.


2.1.3 - 2010-11-30
------------------

* Updated how slurm processes projects


2.1.2 - 2010-09-23
------------------

* More improvements to slurm parser 


2.1.1 - 2010-09-22
------------------

* Default values for SLURM


2.1 - 2010-09-22
----------------

* Added SLURM log parser
* Moved parsers into own directory
* Debian packaging changes


2.0.3 - 2010-09-03
------------------

* Handle memory values in a cleaner way


2.0.2 - 2010-05-28
------------------

* Parse exec_host in PBS


2.0.1 - 2010-03-19
------------------

* Initial release.
