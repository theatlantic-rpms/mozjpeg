# Path under which mozjpeg should be installed
%define _prefix /opt/mozjpeg

# Path under which executables should be installed
%define _bindir /opt/mozjpeg/bin

# Path under which Java classes and man pages should be installed
%define _datadir /opt/mozjpeg/share

# Path under which docs should be installed
%define _docdir /usr/share/doc/%{name}-%{version}

# Path under which headers should be installed
%define _includedir /opt/mozjpeg/include

%if 0%{?rhel} && 0%{?rhel} < 7
%global scl_autotools 1
%else
%global scl_autotools 0
%endif

%ifarch x86_64
%define _lib lib64
%else
%if "%{_prefix}" == "/opt/mozjpeg"
%define _lib lib32
%endif
%endif

# Path under which man pages should be installed
%define _mandir /opt/mozjpeg/share/man

Summary: A JPEG codec that provides increased compression for JPEG images (at the expense of compression performance)
Name: mozjpeg
Version: 3.3.1
Vendor: Mozilla Research
URL: https://github.com/mozilla/mozjpeg
Group: System Environment/Libraries
Source0: https://github.com/mozilla/mozjpeg/archive/v%{version}.tar.gz
Release: 20181219
License: BSD-style
%ifarch x86_64
Provides: %{name} = %{version}-%{release}, mozjpeg = %{version}-%{release}, libturbojpeg.so()(64bit)
%else
Provides: %{name} = %{version}-%{release}, mozjpeg = %{version}-%{release}, libturbojpeg.so
%endif

BuildRequires: nasm
BuildRequires: gcc

%if 0%{?scl_autotools}
BuildRequires: autotools-latest
%else
BuildRequires: autoconf automake libtool
%endif

%description
mozjpeg is a fork of libjpeg-turbo that aims to speed up load times of web
pages by reducing the size (and, by extension, the transmission time) of JPEG
files.  It accomplishes this by enabling optimized Huffman trees and
progressive entropy coding by default in the JPEG compressor, as well as
splitting the spectrum of DCT coefficients into separate scans and using
Trellis quantisation.

Although it is based on libjpeg-turbo, mozjpeg is not intended to be a
general-purpose or high-performance JPEG library.  Its performance is highly
"asymmetric".  That is, the JPEG files it generates require much more time to
compress than to decompress.  When the default settings are used, mozjpeg is
considerably slower than libjpeg-turbo or even libjpeg at compressing images.
Thus, it is not generally suitable for real-time compression.  It is best used
as part of a web encoding workflow.

%prep
%setup -q -n mozjpeg-%{version}
%if 0%{?scl_autotools}
. /opt/rh/autotools-latest/enable
autoreconf -fiv -I/usr/share/aclocal
%else
autoreconf -fiv
%endif

%build
%if 0%{?scl_autotools}
. /opt/rh/autotools-latest/enable
%endif
%configure prefix=%{_prefix} bindir=%{_bindir} datadir=%{_datadir} \
	docdir=%{_docdir} includedir=%{_includedir} libdir=%{_libdir} \
	mandir=%{_mandir} JPEG_LIB_VERSION=62 \
	SO_MAJOR_VERSION=62 SO_MINOR_VERSION=0 \
	--with-pic 
%make_build

%install
%make_install docdir=%{_docdir} exampledir=%{_docdir}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir %{_docdir}
%doc %{_docdir}/*
%dir %{_prefix}
%dir %{_bindir}
%{_bindir}/cjpeg
%{_bindir}/djpeg
%{_bindir}/jpegtran
%{_bindir}/tjbench
%{_bindir}/rdjpgcom
%{_bindir}/wrjpgcom
%dir %{_libdir}
%exclude  %{_libdir}/*.la
%{_libdir}/libjpeg.so.62.2.0
%{_libdir}/libjpeg.so.62
%{_libdir}/libjpeg.so
%{_libdir}/libjpeg.a
%{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libjpeg.pc
%{_libdir}/libturbojpeg.so.0.1.0
%{_libdir}/libturbojpeg.so.0
%{_libdir}/libturbojpeg.so
%{_libdir}/libturbojpeg.a
%{_libdir}/pkgconfig/libturbojpeg.pc
%dir %{_includedir}
%{_includedir}/jconfig.h
%{_includedir}/jerror.h
%{_includedir}/jmorecfg.h
%{_includedir}/jpeglib.h
%{_includedir}/turbojpeg.h
%dir %{_mandir}
%dir %{_mandir}/man1
%{_mandir}/man1/cjpeg.1*
%{_mandir}/man1/djpeg.1*
%{_mandir}/man1/jpegtran.1*
%{_mandir}/man1/rdjpgcom.1*
%{_mandir}/man1/wrjpgcom.1*
%dir %{_datadir}

%changelog
* Wed Dec 19 2018 Frankie Dintino <fdintino@theatlantic.com> - 3.3.1-20181219
- Initial commit
