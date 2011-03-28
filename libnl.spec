#
# Conditional build:
%bcond_without	apidocs		# don't build api docs
#
Summary:	Netlink sockets library
Summary(pl.UTF-8):	Biblioteka do obsługi gniazd netlink
Name:		libnl
Version:	3.0
Release:	3
Epoch:		1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://www.infradead.org/~tgr/libnl/files/%{name}-%{version}.tar.gz
# Source0-md5:	00740414d4d6f173a7dd2aa19432da62
URL:		http://www.infradead.org/~tgr/libnl/
%{?with_apidocs:BuildRequires:	doxygen}
%{?with_apidocs:BuildRequires:	graphviz}
BuildRequires:	linux-libc-headers >= 6:2.6.23
%{?with_apidocs:BuildRequires:	tetex-dvips}
%{?with_apidocs:BuildRequires:	tetex-format-latex}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		skip_post_check_so	bfifo.so.0.0.0 blackhole.so.0.0.0 htb.so.0.0.0 pfifo.so.0.0.0 basic.so.0.0.0 cgroup.so.0.0.0

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
Conflicts:	libnl1-devel

%description devel
Header files for libnl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnl.

%package static
Summary:	Static libnl library
Summary(pl.UTF-8):	Statyczna biblioteka libnl
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}
Conflicts:	libnl1-static

%description static
Static libnl library.

%description static -l pl.UTF-8
Statyczna biblioteka libnl.

%package apidocs
Summary:	libnl library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki libnl
Group:		Documentation

%description apidocs
Documentation for libnl library API and guides in HTML format
generated from sources by doxygen.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libnl oraz wprowadzenie w formacie HTML
wygenerowane ze źródeł za pomocą doxygena.

%prep
%setup -q

%build
%configure \
	--disable-silent-rules

%{__make}
%{?with_apidocs:%{__make} -C doc gendoc}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

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
%attr(755,root,root) %{_sbindir}/nl-class-*
%attr(755,root,root) %{_sbindir}/nl-classid-lookup
%attr(755,root,root) %{_sbindir}/nl-cls-*
%attr(755,root,root) %{_sbindir}/nl-link-list
%attr(755,root,root) %{_sbindir}/nl-pktloc-lookup
%attr(755,root,root) %{_sbindir}/nl-qdisc-*
%attr(755,root,root) %{_libdir}/libnl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl.so.3
%attr(755,root,root) %{_libdir}/libnl-cli.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-cli.so.3
%attr(755,root,root) %{_libdir}/libnl-genl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-genl.so.3
%attr(755,root,root) %{_libdir}/libnl-nf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-nf.so.3
%attr(755,root,root) %{_libdir}/libnl-route.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libnl-route.so.3
%dir %{_libdir}/libnl
%dir %{_libdir}/libnl/cli
%dir %{_libdir}/libnl/cli/cls
%attr(755,root,root) %{_libdir}/libnl/cli/cls/*.so*
%dir %{_libdir}/libnl/cli/qdisc
%attr(755,root,root) %{_libdir}/libnl/cli/qdisc/*.so*
%{_mandir}/man8/nl-classid-lookup.8*
%{_mandir}/man8/nl-pktloc-lookup.8*
%{_mandir}/man8/nl-qdisc-*.8*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnl.so
%attr(755,root,root) %{_libdir}/libnl-cli.so
%attr(755,root,root) %{_libdir}/libnl-genl.so
%attr(755,root,root) %{_libdir}/libnl-nf.so
%attr(755,root,root) %{_libdir}/libnl-route.so
# keep *.la: pkgconfig support is incomplete
%{_libdir}/libnl.la
%{_libdir}/libnl-cli.la
%{_libdir}/libnl-genl.la
%{_libdir}/libnl-nf.la
%{_libdir}/libnl-route.la
%{_includedir}/netlink
%{_pkgconfigdir}/libnl-3.0.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnl.a
%{_libdir}/libnl-cli.a
%{_libdir}/libnl-genl.a
%{_libdir}/libnl-nf.a
%{_libdir}/libnl-route.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/html/*
%endif
