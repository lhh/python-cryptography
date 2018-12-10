%if 0%{?fedora} || 0%{?rhel} >= 8
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%{!?python3_pkgversion:%global python3_pkgversion 3}

%global srcname cryptography

Name:           python-%{srcname}
Version:        2.1.4
Release:        4%{?dist}
Summary:        PyCA's cryptography library

Group:          Development/Libraries
License:        ASL 2.0 or BSD
URL:            https://cryptography.io/en/latest/
Source0:        https://pypi.io/packages/source/c/%{srcname}/%{srcname}-%{version}.tar.gz
Patch0:         0001-disallow-implicit-tag-truncation-with-finalize_with_.patch

BuildRequires:  openssl-devel
BuildRequires:  gcc

BuildRequires:  python2-devel
BuildRequires:  pytest
BuildRequires:  python2-setuptools
BuildRequires:  python-pretend
BuildRequires:  python2-iso8601
BuildRequires:  python2-cryptography-vectors = %{version}
BuildRequires:  python2-asn1crypto >= 0.21
BuildRequires:  python2-hypothesis >= 1.11.4
BuildRequires:  python2-pytz

BuildRequires:  python2-idna >= 2.1
BuildRequires:  python2-six >= 1.4.1
BuildRequires:  python2-cffi >= 1.7
BuildRequires:  python-enum34
BuildRequires:  python-ipaddress

%if 0%{?with_python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pretend
BuildRequires:  python%{python3_pkgversion}-iso8601
BuildRequires:  python%{python3_pkgversion}-cryptography-vectors = %{version}
BuildRequires:  python%{python3_pkgversion}-asn1crypto >= 0.21
BuildRequires:  python%{python3_pkgversion}-hypothesis >= 1.11.4
BuildRequires:  python%{python3_pkgversion}-pytz

BuildRequires:  python%{python3_pkgversion}-idna >= 2.1
BuildRequires:  python%{python3_pkgversion}-six >= 1.4.1
BuildRequires:  python%{python3_pkgversion}-cffi >= 1.7
%endif

%description
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%package -n  python2-%{srcname}
Group:          Development/Libraries
Summary:        PyCA's cryptography library

%if 0%{?with_python3}
%{?python_provide:%python_provide python2-%{srcname}}
%else
Provides:       python-%{srcname} = %{version}-%{release}
Obsoletes:      python-%{srcname} < 2.1.4
%endif

Requires:       openssl-libs
Requires:       python2-idna >= 2.1
Requires:       python2-asn1crypto >= 0.21
Requires:       python2-six >= 1.4.1
Requires:       python2-cffi >= 1.7
Requires:       python-enum34
Requires:       python-ipaddress

%description -n python2-%{srcname}
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.

%if 0%{?with_python3}
%package -n  python%{python3_pkgversion}-%{srcname}
Group:          Development/Libraries
Summary:        PyCA's cryptography library
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

Requires:       openssl-libs
Requires:       python%{python3_pkgversion}-idna >= 2.1
Requires:       python%{python3_pkgversion}-asn1crypto >= 0.21
Requires:       python%{python3_pkgversion}-six >= 1.4.1
Requires:       python%{python3_pkgversion}-cffi >= 1.7

%description -n python%{python3_pkgversion}-%{srcname}
cryptography is a package designed to expose cryptographic primitives and
recipes to Python developers.
%endif

%prep
%autosetup -p1 -n %{srcname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!/usr/bin/python|#!%{__python3}|'
%endif

%build
%if 0%{?with_python3}
%py2_build
pushd %{py3dir}
%py3_build
popd
%else
%{__python2} setup.py build
%endif # with_python3

%install
# Actually other *.c and *.h are appropriate
# see https://github.com/pyca/cryptography/issues/1463
find . -name .keep -print -delete

%if 0%{?with_python3}
%py2_install
pushd %{py3dir}
%py3_install
popd
%else
%{__python2} setup.py install --skip-build --prefix=%{_prefix} --root %{buildroot}
%endif # with_python3


%check
# workaround for pytest 3.2.0 bug https://github.com/pytest-dev/pytest/issues/2644
rm -f tests/hazmat/primitives/test_padding.py
# Disable tests until we have pytest >= 3.2.1
%{__python} setup.py test || :

%if 0%{?with_python3}
pushd %{py3dir}
# workaround for pytest 3.2.0 bug https://github.com/pytest-dev/pytest/issues/2644
rm -f tests/hazmat/primitives/test_padding.py
# Disable tests until we have pytest >= 3.2.1
%{__python3} setup.py test || :
popd
%endif


%files -n python2-%{srcname}
%doc LICENSE LICENSE.APACHE LICENSE.BSD README.rst docs
%{python2_sitearch}/%{srcname}
%{python2_sitearch}/%{srcname}-%{version}-py*.egg-info


%if 0%{?with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%doc README.rst docs
%license LICENSE LICENSE.APACHE LICENSE.BSD
%{python3_sitearch}/*
%{python3_sitearch}/%{srcname}-%{version}-py*.egg-info
%endif


%changelog
* Mon Dec 10 2018 Lon Hohberger <lon@redhat.com> 2.1.4-4
- Rebuild (rhbz#1657935)

* Mon Oct 01 2018 Lon Hohberger <lhh@redhat.com> 2.1.4-3
- Backport fix for CVE-2018-10903

* Tue Apr 24 2018 Jon Schlueter <jschluet@redhat.com> 2.1.4-2
- add Obsoletes for python-cryptography and versioned Provides (rhbz#1571358)

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.4-1
- New upstream release 2.1.4

* Sun Feb 18 2018 Christian Heimes <cheimes@redhat.com> - 2.1.3-4
- Build requires gcc

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.1.3-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 23 2017 Haïkel Guémar <hguemar@fedoraproject.org> - 2.1.3-1
- Upstream 2.1.3

* Tue Oct 24 2017 Christian Heimes <cheimes@redhat.com> - 2.1-2
- Change Requires to openssl-libs

* Thu Oct 12 2017 Christian Heimes <cheimes@redhat.com> - 2.1-1
- New upstream release 2.1

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 2.0.2-3
- Cleanup spec file conditionals

* Thu Aug 03 2017 Christian Heimes <cheimes@redhat.com> - 2.0.2-2
- Add workaround for pytest bug

* Thu Aug 03 2017 Christian Heimes <cheimes@redhat.com> - 2.0.2-1
- New upstream release 2.0.2
- Modernize spec

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Christian Heimes <cheimes@redhat.com> - 1.9-1
- Upstream release 1.9

* Wed Feb 15 2017 Christian Heimes <cheimes@redhat.com> - 1.7.2-1
- Update to latest upstream

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Matěj Cepl <mcepl@redhat.com> - 1.7.1-1
- Update to the latest upstream.
- Add a patch from https://github.com/pyca/cryptography/pull/3328

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.5.3-5
- Enable tests

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.5.3-4
- Rebuild for Python 3.6
- Disable python3 tests for now

* Thu Nov 10 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.5.3-3
- Revert previous change

* Thu Nov 10 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.5.3-2
- Disable tests on releases earlier than 24

* Mon Nov 07 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.5.3-1
- Update to v1.5.3
- Update source URL
- Add BR for pytz

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 10 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.3.1-3
- Remove versioned setuptools dependency

* Tue May 10 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.3.1-2
- Make it easier to build on EL7

* Tue May 03 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.3.1-1
- Update to v1.3.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.2.1-2
- Move python-cryptograph => python2-cryptography

* Sat Jan 09 2016 Nathaniel McCallum <npmccallum@redhat.com> - 1.2.1-1
- Update to v1.2.1

* Wed Nov 11 2015 Robert Kuska <rkuska@redhat.com> - 1.1-1
- Update to v1.1

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 1.0.2-2
- Rebuilt for Python3.5 rebuild

* Wed Sep 30 2015 Matěj Cepl <mcepl@redhat.com> - 1.0.2-1
- New upstream release (fix #1267548)

* Wed Aug 12 2015 Nathaniel McCallum <npmccallum@redhat.com> - 1.0-1
- New upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 14 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.9-1
- New upstream release
- Run tests on RHEL
- New deps: python-idna, python-ipaddress

* Fri Apr 17 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8.2-1
- New upstream release
- Add python3-pyasn1 Requires (#1211073)

* Tue Apr 14 2015 Matej Cepl <mcepl@redhat.com> - 0.8-2
- Add python-pyasn1 Requires (#1211073)

* Fri Mar 13 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.8-1
- New upstream release
- Remove upstreamed patch

* Wed Mar 04 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.7.2-2
- Add python3-cryptography-vectors build requires
- Add python-enum34 requires

* Tue Feb 03 2015 Nathaniel McCallum <npmccallum@redhat.com> - 0.7.2-1
- New upstream release. BSD is now an optional license.
- Fix test running on python3
- Add upstream patch to fix test paths

* Fri Nov 07 2014 Matej Cepl <mcepl@redhat.com> - 0.6.1-2
- Fix requires, for reasons why other development files were not
  eliminated see https://github.com/pyca/cryptography/issues/1463.

* Wed Nov 05 2014 Matej Cepl <mcepl@redhat.com> - 0.6.1-1
- New upstream release.

* Sun Jun 29 2014 Terry Chia <terrycwk1994@gmail.com> 0.4-1
- initial version
