%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}
%endif
%{!?with_python27: %global with_python27 %(%{__python2} -c "import sys; print(sys.version_info>=(2,7,0) and '1' or '0');")}

%global srcname python-alogger

Name: python-alogger
Version: %(cat VERSION.txt)
Release: 1%{?dist}
Summary: Small Python library to parse resource manager logs
%{?el6:Requires: python-importlib}

Group: Development/Libraries
License: GPL3+
Url: https://github.com/Karaage-Cluster/python-alogger

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires:  python2-devel, python-setuptools
%{?el6:BuildRequires: python-importlib}
%if 0%{?with_python3}
BuildRequires:  python3-devel, python3-setuptools, python3-flake8
%endif # if with_python2

%description
Python alogger is a small Python library to parse resource manager logs.
It is used by Karaage. For more information on
Karaage, see https://github.com/Karaage-Cluster/karaage, or the documentation
at http://karaage.readthedocs.org/

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

%build
%{__python2} setup.py build

%if 0%{?with_python3}
%{__python3} setup.py build
%endif # with_python3

%install
rm -rf %{buildroot}

%{__python2} setup.py install  --skip-build --root $RPM_BUILD_ROOT

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
%endif # with_python3

%check
OLD_TZ="$TZ"
export TZ='Australia/Melbourne'

%if 0%{?with_python27}
#%{__python2} /usr/bin/flake8 .
%{__python2} setup.py test
%endif # with_python3

%if 0%{?with_python3}
%{__python2} /usr/bin/flake8 .
%{__python3} setup.py test
%endif # with_python3

TZ="$OLD_TZ"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{python2_sitelib}/*

%if 0%{?with_python3}
%files -n python3-alogger
%{python3_sitelib}/*
%endif # with_python3
