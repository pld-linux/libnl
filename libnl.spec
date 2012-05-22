#
# Conditional build:
%bcond_without	apidocs		# don't build api docs
#
Summary:	Netlink sockets library
Summary(pl.UTF-8):	Biblioteka do obsługi gniazd netlink
Name:		libnl
Version:	3.2.9
Release:	1
Epoch:		1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://www.infradead.org/~tgr/libnl/files/%{name}-%{version}.tar.gz
# Source0-md5:	c13adec0239b266207fff07d79e5ce9e
Patch0:		%{name}-link.patch
Patch1:		%{name}-pedantic.patch
Patch2:		libnl.git-183e86913aab58acf7b5b9cd160518e527bb0348.patch
Patch3:		libnl.git-2fbab02ba8c7b0a418c9d89c2c6db89dd4efd0eb.patch
Patch4:		libnl.git-fec10a282355def49133e63b8a4591cc51b46478.patch
URL:		http://www.infradead.org/~tgr/libnl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison >= 2.4.0
BuildRequires:	flex >= 2.5.34
BuildRequires:	libtool
BuildRequires:	linux-libc-headers >= 6:2.6.23
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	swig-python
%if %{with apidocs}
BuildRequires:	asciidoc >= 8.6.5
BuildRequires:	asciidoc-filter-mscgen >= 1.2
BuildRequires:	doxygen >= 1.8.0
BuildRequires:	mscgen
BuildRequires:	python-pygments
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
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules

%{__make}
%{?with_apidocs:%{__make} -j1 -C doc gendoc}

cd python
CFLAGS="%{rpmcflags}" \
LDFLAGS="%{rpmldflags} -L$(pwd)/../lib/.libs" \
%{__python} setup.py build

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
%attr(755,root,root) %{_libdir}/libnl-nf-3.so
%attr(755,root,root) %{_libdir}/libnl-route-3.so
%{_libdir}/libnl-3.la
%{_libdir}/libnl-cli-3.la
%{_libdir}/libnl-genl-3.la
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
%{_libdir}/libnl-nf-3.a
%{_libdir}/libnl-route-3.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc doc/{*.html,api,images}
%endif

%files -n python-netlink
%defattr(644,root,root,755)
%dir %{py_sitedir}/netlink
%attr(755,root,root) %{py_sitedir}/netlink/_capi.so
%{py_sitedir}/netlink/*.py[co]
%dir %{py_sitedir}/netlink/route
%attr(755,root,root) %{py_sitedir}/netlink/route/_capi.so
%{py_sitedir}/netlink/route/*.py[co]
%dir %{py_sitedir}/netlink/route/links
%{py_sitedir}/netlink/route/links/*.py[co]
%dir %{py_sitedir}/netlink/route/qdisc
%{py_sitedir}/netlink/route/qdisc/*.py[co]
%{py_sitedir}/netlink-1.0-py*.egg-info
