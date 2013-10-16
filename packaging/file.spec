Summary: A utility for determining file types
Name: file
Version: 5.04
Release: 1
License: BSD
Group: Applications/File
Source0: ftp://ftp.astron.com/pub/file/file-%{version}.tar.gz
URL: http://www.darwinsys.com/file/
Patch0: file-4.21-pybuild.patch
Patch1: file-4.26-devdrv.patch
Patch2: file-4.26-mime-encoding.patch
BuildRequires: zlib-devel

%description
The file command is used to identify a particular file according to the
type of data contained by the file.  File can identify many different
file types, including ELF binaries, system libraries, RPM packages, and
different graphics formats.

You should install the file package, since the file command is such a
useful utility.

%package -n libfile
Summary: Libraries for applications using libmagic
Group:   Applications/File

%description -n libfile
Libraries for applications using libmagic.

%package -n libfile-devel
Summary:  Libraries and header files for file development
Group:    Applications/File
Requires: libfile = %{version}-%{release}

%description -n libfile-devel
The file-devel package contains the header files and libmagic library
necessary for developing programs using libmagic.


%prep
# Don't use -b -- it will lead to poblems when compiling magic file
%setup -q
%patch0 -p1
#fixes #463809
%patch1 -p1
#fixes #465994
%patch2 -p1

iconv -f iso-8859-1 -t utf-8 < doc/libmagic.man > doc/libmagic.man_
touch -r doc/libmagic.man doc/libmagic.man_
mv doc/libmagic.man_ doc/libmagic.man

%build
CFLAGS="%{optflags} -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE" \
%configure --enable-fsect-man5 --disable-rpath
# remove hardcoded library paths from local libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/src/.libs
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man5
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/misc
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/file
mkdir -p %{buildroot}/usr/share/license
cp COPYING %{buildroot}/usr/share/license/%{name}

%make_install

cat magic/Magdir/* > ${RPM_BUILD_ROOT}%{_datadir}/file/magic
ln -s file/magic ${RPM_BUILD_ROOT}%{_datadir}/magic
#ln -s file/magic.mime ${RPM_BUILD_ROOT}%{_datadir}/magic.mime
ln -s ../magic ${RPM_BUILD_ROOT}%{_datadir}/misc/magic



%post -n libfile -p /sbin/ldconfig

%postun -n libfile -p /sbin/ldconfig

%docs_package

%files
%defattr(-,root,root,-)
%{_bindir}/*
/usr/share/license/%{name}

%files -n libfile
%{_libdir}/*so.*
%{_datadir}/magic*
%{_datadir}/file
%{_datadir}/misc/*

%files -n libfile-devel
%{_libdir}/*.so
%{_includedir}/magic.h

