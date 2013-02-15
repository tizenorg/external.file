%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}
%define __libtoolize :

Summary: Python bindings for the libmagic API
Name: python-magic
Version: 5.04
Release: 3
License: BSD
Group: System/Libraries
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
URL: http://www.darwinsys.com/file/
Patch0: file-4.21-pybuild.patch
Patch1: file-4.26-devdrv.patch
Patch2: file-4.26-mime-encoding.patch

Requires: file >= %{version}
BuildRequires: zlib-devel
BuildRequires: python-devel, file-devel

%description
This package contains the Python bindings to allow access to the
libmagic API. The libmagic library is also used by the familiar
file(1) command.

%prep
# Don't use -b -- it will lead to poblems when compiling magic file
%setup -q -n file-%{version}
%patch0 -p1
#fixes #463809
%patch1 -p1
#fixes #465994
%patch2 -p1


%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
cd python
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
cd python
%{__python} setup.py install -O1 --skip-build --root ${RPM_BUILD_ROOT}
%{__install} -d ${RPM_BUILD_ROOT}%{_datadir}/%{name}
%{__install} -D example.py ${RPM_BUILD_ROOT}/%{_docdir}/python-magic-%{version}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc python/README COPYING python/example.py
%{python_sitearch}/magic.so
%{python_sitearch}/*egg-info

