%if 0%{?fedora}
%global with_python3 1
%endif

%global pypi_name XStatic-objectpath

Name:           python-%{pypi_name}
Version:        1.2.1.0
Release:        1%{?dist}
Summary:        ObjectPath JavaScript library (XStatic packaging standard)

License:        MIT
URL:            https://github.com/mike-marcacci/objectpath
Source0:        https://pypi.io/packages/source/X/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/mike-marcacci/objectpath/master/license
BuildArch:      noarch

%description
ObjectPath JavaScript library packaged
for setuptools (easy_install) / pip.

Parse js object paths using both dot and bracket notation.
Stringify an array of properties into a valid path.

%package -n python2-%{pypi_name}
Summary: ObjectPath JavaScript library (XStatic packaging standard)
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python-XStatic
Requires:       xstatic-objectpath-common

%description -n python2-%{pypi_name}
ObjectPath JavaScript library packaged
for setuptools (easy_install) / pip.

Parse js object paths using both dot and bracket notation.
Stringify an array of properties into a valid path.

%package -n xstatic-objectpath-common
Summary: ObjectPath JavaScript library (XStatic packaging standard)

BuildRequires:  web-assets-devel
Requires:       web-assets-filesystem

%description -n xstatic-objectpath-common
ObjectPath JavaScript library packaged
for setuptools (easy_install) / pip.

This package contains the javascript files.

%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary: ObjectPath JavaScript library (XStatic packaging standard)
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3-XStatic
Requires:       xstatic-objectpath-common

%description -n python3-%{pypi_name}
ObjectPath JavaScript library packaged
for setuptools (easy_install) / pip.

Parse js object paths using both dot and bracket notation.
Stringify an array of properties into a valid path.
%endif

%prep
%setup -q -n %{pypi_name}-%{version}
cp %{SOURCE1} .

# patch to use webassets dir
sed -i "s|^BASE_DIR = .*|BASE_DIR = '%{_jsdir}/objectpath'|" xstatic/pkg/objectpath/__init__.py

%build
%{__python2} setup.py build
%if 0%{?with_python3}
%{__python3} setup.py build
%endif

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

# Move static files
mkdir -p %{buildroot}/%{_jsdir}/objectpath
mv %{buildroot}/%{python2_sitelib}/xstatic/pkg/objectpath/data/ObjectPath.js %{buildroot}/%{_jsdir}/objectpath

rmdir %{buildroot}/%{python2_sitelib}/xstatic/pkg/objectpath/data/

%if 0%{?with_python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
# Remove static files, already created by the python2 subpkg
rm -rf %{buildroot}/%{python3_sitelib}/xstatic/pkg/objectpath/data
%endif

%files -n python2-%{pypi_name}
%doc README.txt
%license license
%{python2_sitelib}/xstatic/pkg/objectpath
%{python2_sitelib}/XStatic_objectpath-%{version}-py?.?.egg-info
%{python2_sitelib}/XStatic_objectpath-%{version}-py?.?-nspkg.pth

%files -n xstatic-objectpath-common
%doc README.txt
%license license
%{_jsdir}/objectpath

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.txt
%license license
%{python3_sitelib}/xstatic/pkg/objectpath
%{python3_sitelib}/XStatic_objectpath-%{version}-py?.?.egg-info
%{python3_sitelib}/XStatic_objectpath-%{version}-py?.?-nspkg.pth
%endif

%changelog
* Fri Aug 5 2016 David Moreau Simard <dmsimard@redhat.com> - 1.2.1.0-1
- First version
