Name:           attr
%define lname	libattr
Summary:        Commands for Manipulating Extended Attributes
License:        GPL-2.0+ ; LGPL-2.1+
Group:          Base/File Systems
Version:        2.4.46
Release:        0
Source:         %{name}-%{version}.src.tar.gz
Source1:        xattr.conf
Source2:        baselibs.conf
Source1001: 	attr.manifest
Url:            http://download.savannah.gnu.org/releases-noredirect/attr/
BuildRequires:  autoconf

%description
A set of tools for manipulating extended attributes on file system
objects, in particular getfattr(1) and setfattr(1). An attr(1) command
is also provided, which is largely compatible with the SGI IRIX tool of
the same name.

%package -n %lname
Summary:        A dynamic library for filesystem extended attribute support
Group:          Base/File Systems

%description -n %lname
This package contains the libattr.so dynamic library, which contains
the extended attribute library functions.

%package -n libattr-devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Provides:       attr-devel
Obsoletes:      attr-devel
Requires:       %lname = %version
Requires:       glibc-devel

%description -n libattr-devel
This package contains the libraries and header files needed to develop
programs which make use of extended attributes. For Linux programs, the
documented system call API is the recommended interface, but an SGI
IRIX compatibility interface is also provided.

%package -n libattr-devel-static
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Libraries
Provides:       libattr-devel:%{_libdir}/libattr.a
Requires:       libattr-devel = %version

%description -n libattr-devel-static
This package contains the static library of libattr which is needed to develop
statically linked programs which make use of extended attributes.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export OPTIMIZER="$RPM_OPT_FLAGS -fPIC"
export DEBUG=-DNDEBUG
autoconf
CFLAGS="$RPM_OPT_FLAGS" \
%configure \
	--prefix=/ \
	--enable-gettext=no \
	--exec-prefix=/ \
	--sbindir=%_sbindir \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--with-pic
%{__make} %{?_smp_mflags}

%install
DIST_ROOT="$RPM_BUILD_ROOT"
DIST_INSTALL=`pwd`/install.manifest
DIST_INSTALL_DEV=`pwd`/install-dev.manifest
DIST_INSTALL_LIB=`pwd`/install-lib.manifest
export DIST_ROOT DIST_INSTALL DIST_INSTALL_DEV DIST_INSTALL_LIB
/usr/bin/make install DIST_MANIFEST="$DIST_INSTALL"
/usr/bin/make install-dev DIST_MANIFEST="$DIST_INSTALL_DEV"
/usr/bin/make install-lib DIST_MANIFEST="$DIST_INSTALL_LIB"
rm -f $RPM_BUILD_ROOT%{_mandir}/man2/*xattr.2*
rm -f $RPM_BUILD_ROOT/%{_libdir}/libattr.la
install -d -m 755 $RPM_BUILD_ROOT/%{_sysconfdir}
install -m 644 %_sourcedir/xattr.conf $RPM_BUILD_ROOT/%{_sysconfdir}
chmod 755 $RPM_BUILD_ROOT/%{_libdir}/libattr.so.1*

%post -n %lname -p /sbin/ldconfig

%postun -n %lname -p /sbin/ldconfig

%docs_package

%files
%manifest %{name}.manifest
%defattr (-,root,root)
%dir %attr(755,root,root) /usr/share/doc/packages/attr
%doc %attr(644,root,root) /usr/share/doc/packages/attr/README
%doc %attr(644,root,root) /usr/share/doc/packages/attr/CHANGES.gz
%doc %attr(644,root,root) /usr/share/doc/packages/attr/COPYING
%doc %attr(644,root,root) /usr/share/doc/packages/attr/PORTING
%attr(755,root,root) %{_bindir}/attr
%attr(755,root,root) %{_bindir}/getfattr
%attr(755,root,root) %{_bindir}/setfattr

%files -n libattr-devel
%manifest %{name}.manifest
%defattr(-,root,root)
%dir %attr(755,root,root) %{_includedir}/attr
%attr(644,root,root) %{_includedir}/attr/attributes.h
%attr(644,root,root) %{_includedir}/attr/error_context.h
%attr(644,root,root) %{_includedir}/attr/libattr.h
%attr(644,root,root) %{_includedir}/attr/xattr.h
%attr(755,root,root) %{_libdir}/libattr.so

%files -n libattr-devel-static
%manifest %{name}.manifest
%defattr(-,root,root)
%{_libdir}/libattr.a

%files -n %lname
%manifest %{name}.manifest
%defattr (-,root,root)
%{_libdir}/libattr.so.1*
%config %{_sysconfdir}/xattr.conf

%changelog
