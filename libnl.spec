Summary:	Netlink library
Summary(pl.UTF-8):	Biblioteka do obsługi gniazd netlink
Name:		libnl
Version:	1.0
%define pre pre7
Release:	0.%{pre}.3
License:	LGPL v2.1
Group:		Libraries
Source0:	http://people.suug.ch/~tgr/libnl/files/%{name}-%{version}-%{pre}.tar.gz
# Source0-md5:	db9f6265c370f09defd2d2fa3540758e
#Patch0:		%{name}-llh.patch
URL:		http://people.suug.ch/~tgr/libnl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	linux-libc-headers >= 7:2.6.20
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
Requires:	%{name} = %{version}-%{release}
Requires:	linux-libc-headers >= 7:2.6.20

%description devel
Header files for libnl library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libnl.

%package static
Summary:	Static libnl library
Summary(pl.UTF-8):	Statyczna biblioteka libnl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libnl library.

%description static -l pl.UTF-8
Statyczna biblioteka libnl.

%prep
%setup -q -n %{name}-%{version}-%{pre}

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

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/libnl.so.[0-9].[0-9]*
%ghost %attr(755,root,root) %{_libdir}/libnl.so.[!.]

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libnl.so
%{_includedir}/netlink
%{_pkgconfigdir}/libnl-1.pc
