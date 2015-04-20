%if 0%{?fedora} > 12
%global with_python27 1
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%{!?with_python27: %global with_python27 %(%{__python2} -c "import sys; print(sys.version_info>=(2,7,0) and '1' or '0');")}
%endif

%global srcname python-alogger

Name: python-alogger
Version: 2.2.6
Release: 1%{?dist}
Summary: Small Python library to parse resource manager logs
%{?el6:Requires: python-importlib}

Group: Development/Libraries
License: GPLv3+
URL: https://github.com/Karaage-Cluster/python-alogger
Source: %{name}_%{version}.tar.gz

BuildArch: noarch

BuildRequires:  python2-devel, python-setuptools
%if 0%{?fedora} > 20
BuildRequires:  python-flake8
%endif # if fedora > 20
%{?el6:BuildRequires: python-importlib}

%if 0%{?with_python3}
BuildRequires:  python3-devel, python3-setuptools
%if 0%{?fedora} > 20
BuildRequires:  python3-flake8
%endif # fedora > 20
%endif # if with_python3

%description
Python alogger is a small Python library to parse resource manager logs.
It is used by Karaage. For more information on
Karaage, see https://github.com/Karaage-Cluster/karaage, or the documentation
at http://karaage.readthedocs.org/

%changelog
* Mon Apr 20 2015 Brian May <brian@microcomaustralia.com.au> 2.2.6-1
- updates to rpm spec file.
- torque: Fix est_wall_time.
- torque (PBS Pro): Fix core count.

* Tue Mar 31 2015 Brian May <brian@microcomaustralia.com.au> 2.2.5-1
- Add new config option.

%if 0%{?with_python3}
%package -n python3-alogger
Summary: Small Python library to parse resource manager logs

%description -n python3-alogger
Python alogger is a small Python library to parse resource manager logs.
It is used by Karaage. For more information on
Karaage, see https://github.com/Karaage-Cluster/karaage, or the documentation
at http://karaage.readthedocs.org/

%endif # with_python2

%prep
%setup -q

%build
%{__python2} setup.py build

%if 0%{?with_python3}
%{__python3} setup.py build
%endif # with_python3

%install
rm -rf %{buildroot}

%{__python2} setup.py install  --skip-build --root $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/python-alogger

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/python3-alogger
%endif # with_python3

%check
OLD_TZ="$TZ"
export TZ='Australia/Melbourne'

# Python 2 tests only work with Python >= 2.7
%if 0%{?fedora} > 20
    %{__python2} /usr/bin/flake8 .
%endif # fedora > 20
%if 0%{?with_python27}
%{__python2} setup.py test
%endif # with_python2

%if 0%{?with_python3}
%if 0%{?fedora} > 20
    %{__python3} /usr/bin/flake8 .
%endif # fedora > 20
%{__python3} setup.py test
%endif # with_python3

TZ="$OLD_TZ"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{python2_sitelib}/*
%doc AUTHORS.txt COPYING.txt README.rst

%if 0%{?with_python3}
%files -n python3-alogger
%{python3_sitelib}/*
%doc AUTHORS.txt COPYING.txt README.rst
%endif # with_python3
