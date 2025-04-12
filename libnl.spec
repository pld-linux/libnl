#
# Conditional build:
%bcond_without	apidocs		# API documentation
%bcond_without	python		# Python netlink module (any)
%bcond_without	python2		# CPython 2.x netlink module
%bcond_without	python3		# CPython 3.x netlink module
%bcond_without	tests		# unit tests
%bcond_with	net_tests	# unit tests using unshare for net ns

Summary:	Netlink sockets library
Summary(pl.UTF-8):	Biblioteka do obsługi gniazd netlink
Name:		libnl
Version:	3.11.0
Release:	1
Epoch:		1
License:	LGPL v2.1
Group:		Libraries
Source0:	https://github.com/thom311/libnl/releases/download/libnl3_11_0/%{name}-%{version}.tar.gz
# Source0-md5:	0a5eb82b494c411931a47638cb0dba51
Source1:	https://github.com/thom311/libnl/releases/download/libnl3_11_0/%{name}-doc-%{version}.tar.gz
# Source1-md5:	5c74044c92f2eb08de69cce88714cd1b
URL:		http://www.infradead.org/~tgr/libnl/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison >= 2.4.0
%{?with_net_tests:BuildRequires:	check >= 0.9.0}
BuildRequires:	flex >= 2.5.34
BuildRequires:	libtool >= 2:2
BuildRequires:	linux-libc-headers >= 6:2.6.23
BuildRequires:	pkgconfig
%{?with_python2:BuildRequires:	python-devel >= 1:2.7}
%{?with_python3:BuildRequires:	python3-devel >= 1:3.2}
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
BuildRequires:	swig-python >= 2
%if 0 && %{with apidocs}
# no docs Makefile up to 3.2.24
BuildRequires:	asciidoc >= 8.6.5
BuildRequires:	asciidoc-filter-mscgen >= 1.2
BuildRequires:	doxygen >= 1.8.0
BuildRequires:	graphviz
BuildRequires:	mscgen
BuildRequires:	python-pygments
BuildRequires:	source-highlight
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libnl is a library for applications dealing with netlink socket. It
provides an easy to use interface for raw netlink message but also
netlink family specific APIs.

%description -l pl.UTF-8
libnl jest biblioteką dla aplikacji rozmawiających z gniazdem netlink.
Udostępnia łatwy w użyciu interfejs do korzystania z surowych
wiadomości netlink, a także API specyficzne dla rodziny gniazd
netlink.

%package devel
Summary:	Header files for libnl library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libnl
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files for libnl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnl.

%package static
Summary:	Static libnl library
Summary(pl.UTF-8):	Statyczna biblioteka libnl
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libnl library.

%description static -l pl.UTF-8
Statyczna biblioteka libnl.

%package apidocs
Summary:	libnl library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libnl
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation for libnl library API and guides in HTML format
generated from sources by doxygen.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnl oraz wprowadzenie w formacie HTML
wygenerowane ze źródeł za pomocą doxygena.

%package -n python-netlink
Summary:	Python 2 wrapper for netlink protocols
Summary(pl.UTF-8):	Interfejs Pythona 2 do protokołów netlink
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-netlink
Python 2 wrapper for netlink protocols.

%description -n python-netlink -l pl.UTF-8
Interfejs Pythona 2 do protokołów netlink.

%package -n python3-netlink
Summary:	Python 3 wrapper for netlink protocols
Summary(pl.UTF-8):	Interfejs Pythona 3 do protokołów netlink
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python3-netlink
Python 3 wrapper for netlink protocols.

%description -n python3-netlink -l pl.UTF-8
Interfejs Pythona 3 do protokołów netlink.

%prep
%setup -q -a1
%{__mv} libnl-doc-%{version} doc

%if %{without net_tests}
%{__sed} -i -e 's/^AM_CONDITIONAL(WITH_CHECK.*/AM_CONDITIONAL(WITH_CHECK, false)/' configure.ac
%endif

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_apidocs:--disable-doc} \
	--disable-silent-rules

%{__make}

%if 0
# no docs Makefile up to 3.2.25
%{?with_apidocs:%{__make} -j1 -C doc gendoc}
%endif

%if %{with python}
cd python
CFLAGS="%{rpmcflags}"
LDFLAGS="%{rpmldflags} -L$(pwd)/../lib/.libs"
%if %{with python2}
%py_build
%endif
%if %{with python3}
%py3_build
%endif
cd ..
%endif

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if %{with python}
cd python
%if %{with python2}
%py_install
%py_postclean
%endif
%if %{with python3}
%py3_install
%endif
%endif

# dynamic modules
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libnl/cli/*/*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%dir %{_sysconfdir}/libnl
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libnl/classid
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/libnl/pktloc
%attr(755,root,root) %{_bindir}/genl-ctrl-list
%attr(755,root,root) %{_bindir}/idiag-socket-details
%attr(755,root,root) %{_bindir}/nf-ct-*
%attr(755,root,root) %{_bindir}/nf-exp-*
%attr(755,root,root) %{_bindir}/nf-log
%attr(755,root,root) %{_bindir}/nf-monitor
%attr(755,root,root) %{_bindir}/nf-queue
%attr(755,root,root) %{_bindir}/nl-addr-*
%attr(755,root,root) %{_bindir}/nl-class-*
%attr(755,root,root) %{_bindir}/nl-classid-lookup
%attr(755,root,root) %{_bindir}/nl-cls-*
%attr(755,root,root) %{_bindir}/nl-fib-lookup
%attr(755,root,root) %{_bindir}/nl-link-*
%attr(755,root,root) %{_bindir}/nl-list-*
%attr(755,root,root) %{_bindir}/nl-monitor
%attr(755,root,root) %{_bindir}/nl-neigh-*
%attr(755,root,root) %{_bindir}/nl-neightbl-list
%attr(755,root,root) %{_bindir}/nl-nh-list
%attr(755,root,root) %{_bindir}/nl-pktloc-lookup
%attr(755,root,root) %{_bindir}/nl-qdisc-*
%attr(755,root,root) %{_bindir}/nl-route-*
%attr(755,root,root) %{_bindir}/nl-rule-list
%attr(755,root,root) %{_bindir}/nl-tctree-list
%attr(755,root,root) %{_bindir}/nl-util-addr
%attr(755,root,root) %{_libdir}/libnl-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-3.so.200
%attr(755,root,root) %{_libdir}/libnl-cli-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-cli-3.so.200
%attr(755,root,root) %{_libdir}/libnl-genl-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-genl-3.so.200
%attr(755,root,root) %{_libdir}/libnl-idiag-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-idiag-3.so.200
%attr(755,root,root) %{_libdir}/libnl-nf-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-nf-3.so.200
%attr(755,root,root) %{_libdir}/libnl-route-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-route-3.so.200
%attr(755,root,root) %{_libdir}/libnl-xfrm-3.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-xfrm-3.so.200
%dir %{_libdir}/libnl
%dir %{_libdir}/libnl/cli
%dir %{_libdir}/libnl/cli/cls
%attr(755,root,root) %{_libdir}/libnl/cli/cls/*.so
%dir %{_libdir}/libnl/cli/qdisc
%attr(755,root,root) %{_libdir}/libnl/cli/qdisc/*.so
%{_mandir}/man8/genl-ctrl-list.8*
%{_mandir}/man8/nl-classid-lookup.8*
%{_mandir}/man8/nl-pktloc-lookup.8*
%{_mandir}/man8/nl-qdisc-*.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnl-3.so
%attr(755,root,root) %{_libdir}/libnl-cli-3.so
%attr(755,root,root) %{_libdir}/libnl-genl-3.so
%attr(755,root,root) %{_libdir}/libnl-idiag-3.so
%attr(755,root,root) %{_libdir}/libnl-nf-3.so
%attr(755,root,root) %{_libdir}/libnl-route-3.so
%attr(755,root,root) %{_libdir}/libnl-xfrm-3.so
%{_libdir}/libnl-3.la
%{_libdir}/libnl-cli-3.la
%{_libdir}/libnl-genl-3.la
%{_libdir}/libnl-idiag-3.la
%{_libdir}/libnl-nf-3.la
%{_libdir}/libnl-route-3.la
%{_libdir}/libnl-xfrm-3.la
%{_includedir}/libnl3
%{_pkgconfigdir}/libnl-3.0.pc
%{_pkgconfigdir}/libnl-cli-3.0.pc
%{_pkgconfigdir}/libnl-genl-3.0.pc
%{_pkgconfigdir}/libnl-idiag-3.0.pc
%{_pkgconfigdir}/libnl-nf-3.0.pc
%{_pkgconfigdir}/libnl-route-3.0.pc
%{_pkgconfigdir}/libnl-xfrm-3.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnl-3.a
%{_libdir}/libnl-cli-3.a
%{_libdir}/libnl-genl-3.a
%{_libdir}/libnl-idiag-3.a
%{_libdir}/libnl-nf-3.a
%{_libdir}/libnl-route-3.a
%{_libdir}/libnl-xfrm-3.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/{*.html,libnl.css,api,images,stylesheets}
%endif

%if %{with python2}
%files -n python-netlink
%defattr(644,root,root,755)
%dir %{py_sitedir}/netlink
%attr(755,root,root) %{py_sitedir}/netlink/_capi.so
%{py_sitedir}/netlink/*.py[co]
%dir %{py_sitedir}/netlink/genl
%attr(755,root,root) %{py_sitedir}/netlink/genl/_capi.so
%{py_sitedir}/netlink/genl/*.py[co]
%dir %{py_sitedir}/netlink/route
%attr(755,root,root) %{py_sitedir}/netlink/route/_capi.so
%{py_sitedir}/netlink/route/*.py[co]
%dir %{py_sitedir}/netlink/route/links
%{py_sitedir}/netlink/route/links/*.py[co]
%dir %{py_sitedir}/netlink/route/qdisc
%{py_sitedir}/netlink/route/qdisc/*.py[co]
%{py_sitedir}/netlink-1.0-py*.egg-info
%endif

%if %{with python3}
%files -n python3-netlink
%defattr(644,root,root,755)
%dir %{py3_sitedir}/netlink
%attr(755,root,root) %{py3_sitedir}/netlink/_capi.cpython-*.so
%{py3_sitedir}/netlink/*.py
%{py3_sitedir}/netlink/__pycache__
%dir %{py3_sitedir}/netlink/genl
%attr(755,root,root) %{py3_sitedir}/netlink/genl/_capi.cpython-*.so
%{py3_sitedir}/netlink/genl/*.py
%{py3_sitedir}/netlink/genl/__pycache__
%dir %{py3_sitedir}/netlink/route
%attr(755,root,root) %{py3_sitedir}/netlink/route/_capi.cpython-*.so
%{py3_sitedir}/netlink/route/*.py
%{py3_sitedir}/netlink/route/__pycache__
%dir %{py3_sitedir}/netlink/route/links
%{py3_sitedir}/netlink/route/links/*.py
%{py3_sitedir}/netlink/route/links/__pycache__
%dir %{py3_sitedir}/netlink/route/qdisc
%{py3_sitedir}/netlink/route/qdisc/*.py
%{py3_sitedir}/netlink/route/qdisc/__pycache__
%{py3_sitedir}/netlink-1.0-py*.egg-info
%endif
