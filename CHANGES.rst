Release 2.2.6-2 (26 Apr 2016)
=============================

* Fix flake8 issues.


Release 2.2.6-1 (20 Apr 2015)
=============================

* torque: Fix est_wall_time.
* torque (PBS Pro): Fix core count.


Release 2.2.5-1 (31 Mar 2015)
=============================

* New config options to allow replacing default project.


Release 2.2.4-1 (06 Mar 2015)
=============================

* PBS Pro uses 'project' not 'account'.
* Simplify act_wall_time processing.
* est_wall_time is optional and can be None.


Release 2.2.3-1 (31 Oct 2014)
=============================

* Support PBS parser as legacy alias for TORQUE.
* Ignore file not found error when reading TORQUE log file.
* Fix RPM package version.


Release 2.2.2-1 (30 Oct 2014)
=============================

* Include test data.
* New API to read from source. Note: Slurm reader still incomplete, memory
  usage information will not be read.
* Update sample torque log file.


Release 2.2.1-1 (27 Oct 2014)
=============================

* New version.
* More tests.


Release 2.2.0-1 (07 Jul 2014)
=============================

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


Release 2.1.7-1 (19 May 2014)
=============================

* Updates for Slurm support. Contributed by VLSCI.


Release 2.1.6-1 (11 Mar 2014)
=============================

* Update python packaging.
* Update information.
* No functional changes.


Release 2.1.5-1 (29 Jan 2014)
=============================

* Update Debian packaging.


Release 2.1.4-1 (28 May 2013)
=============================

* Update Debian packaging.
* Slurm specific changes from 2010.
* Initial attempt for Windows HPC support from 2011.


Release 2.1.3-1 (30 Nov 2010)
=============================

* Updated how slurm processes projects


Release 2.1.2-1 (23 Sep 2010)
=============================

* More improvements to slurm parser 


Release 2.1.1-1 (22 Sep 2010)
=============================

* Default values for SLURM


Release 2.1-1 (22 Sep 2010)
=============================

* Added SLURM log parser
* Moved parsers into own directory
* Debian packaging changes


Release 2.0.3 (03 Sep 2010)
=============================

* Handle memory values in a cleaner way


Release 2.0.2 (28 May 2010)
===========================

* Parse exec_host in PBS


Release 2.0.1 (19 Mar 2010)
===========================

* Initial release.