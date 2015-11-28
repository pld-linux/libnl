#
# Conditional build:
%bcond_without	apidocs		# don't build api docs
%bcond_without	tests		# don't perform "make check"

Summary:	Netlink sockets library
Summary(pl.UTF-8):	Biblioteka do obsługi gniazd netlink
Name:		libnl
Version:	3.2.25
Release:	3
Epoch:		1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://www.infradead.org/~tgr/libnl/files/%{name}-%{version}.tar.gz
# Source0-md5:	03f74d0cd5037cadc8cdfa313bbd195c
Source1:	http://www.infradead.org/~tgr/libnl/files/%{name}-doc-%{version}.tar.gz
# Source1-md5:	641f73052d9f54e720efe1a476a20237
Patch0:		%{name}-link.patch
Patch1:		%{name}-pedantic.patch
URL:		http://www.infradead.org/~tgr/libnl/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	bison >= 2.4.0
%{?with_tests:BuildRequires:	check >= 0.9.0}
BuildRequires:	flex >= 2.5.34
BuildRequires:	libtool
BuildRequires:	linux-libc-headers >= 6:2.6.23
BuildRequires:	pkgconfig
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig-python
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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
Documentation for libnl library API and guides in HTML format
generated from sources by doxygen.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnl oraz wprowadzenie w formacie HTML
wygenerowane ze źródeł za pomocą doxygena.

%package -n python-netlink
Summary:	Python wrapper for netlink protocols
Summary(pl.UTF-8):	Pythonowy interfejs do protokołów netlink
Group:		Libraries/Python
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description -n python-netlink
Python wrapper for netlink protocols.

%description -n python-netlink -l pl.UTF-8
Pythonowy interfejs do protokołów netlink.

%prep
%setup -q -a1
mv -f libnl-doc-%{version} doc
%patch0 -p1
%patch1 -p1

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

cd python
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags} -L$(pwd)/../lib/.libs" \
%{__python} setup.py build

%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd python
%{__python} setup.py install \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%py_postclean

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
%attr(755,root,root) %{_sbindir}/genl-ctrl-list
%attr(755,root,root) %{_sbindir}/nl-class-*
%attr(755,root,root) %{_sbindir}/nl-classid-lookup
%attr(755,root,root) %{_sbindir}/nl-cls-*
%attr(755,root,root) %{_sbindir}/nl-link-list
%attr(755,root,root) %{_sbindir}/nl-pktloc-lookup
%attr(755,root,root) %{_sbindir}/nl-qdisc-*
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
%{_libdir}/libnl-3.la
%{_libdir}/libnl-cli-3.la
%{_libdir}/libnl-genl-3.la
%{_libdir}/libnl-idiag-3.la
%{_libdir}/libnl-nf-3.la
%{_libdir}/libnl-route-3.la
%{_includedir}/libnl3
%{_pkgconfigdir}/libnl-3.0.pc
%{_pkgconfigdir}/libnl-cli-3.0.pc
%{_pkgconfigdir}/libnl-genl-3.0.pc
%{_pkgconfigdir}/libnl-nf-3.0.pc
%{_pkgconfigdir}/libnl-route-3.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnl-3.a
%{_libdir}/libnl-cli-3.a
%{_libdir}/libnl-genl-3.a
%{_libdir}/libnl-idiag-3.a
%{_libdir}/libnl-nf-3.a
%{_libdir}/libnl-route-3.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/{*.html,libnl.css,api,images,stylesheets}
%endif

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
