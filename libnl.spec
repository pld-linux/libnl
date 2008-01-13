Summary:	Netlink library
Summary(pl.UTF-8):	Biblioteka do obsługi gniazd netlink
Name:		libnl
Version:	1.0
Release:	1
Epoch:		1
License:	LGPL v2.1
Group:		Libraries
Source0:	http://people.suug.ch/~tgr/libnl/files/%{name}-%{version}.tar.gz
# Source0-md5:	fd59c63cfa8ad50c8331a48aa252e483
Patch0:		%{name}-static.patch
URL:		http://people.suug.ch/~tgr/libnl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libnl is a library for applications dealing with netlink socket. It
provides an easy to use interface for raw netlink message but also
netlink family specific APIs.

%description -l pl.UTF-8
libnl jest biblioteką dla aplikacji rozmawiających z gniazdem
netlink. Udostępnia łatwy w użyciu interfejs do korzystania z
surowych wiadomości netlink, a także API specyficzne dla rodziny
gniazd netlink.

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

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__autoconf}

%configure \
	--enable-verbose-errors

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# for autodeps to work
chmod +x $RPM_BUILD_ROOT%{_libdir}/libnl.so.*.*

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libnl.so.*.*
%ghost %attr(755,root,root) %{_libdir}/libnl.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnl.so
%{_includedir}/netlink
%{_pkgconfigdir}/libnl-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libnl.a
