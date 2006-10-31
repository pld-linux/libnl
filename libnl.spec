Summary:	Netlink library
Summary(pl):	Biblioteka do obs³ugi gniazd netlink
Name:		libnl
Version:	1.0
%define pre pre5
Release:	0.%{pre}.2
License:	LGPL v2.1
Group:		Libraries
Source0:	http://people.suug.ch/~tgr/libnl/files/%{name}-%{version}-%{pre}.tar.gz
# Source0-md5:	2cece8968bb36b4cc34b907b6e3c2178
Source1:	%{name}-1.pc
Patch0:		%{name}-no_root.patch
Patch1:		%{name}-llh.patch
URL:		http://people.suug.ch/~tgr/libnl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libnl is a library for applications dealing with netlink socket. It
provides an easy to use interface for raw netlink message but also
netlink family specific APIs.

%description -l pl
libnl jest bibliotek± dla aplikacji rozmawiaj±cych z gniazdem
netlink. Udostêpnia ³atwy w u¿yciu interfejs do korzystania z
surowych wiadomo¶ci netlink, a tak¿e API specyficzne dla rodziny
gniazd netlink.

%package devel
Summary:	Header files for libnl library
Summary(pl):	Pliki nag³ówkowe biblioteki libnl
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libnl library.

%description devel -l pl
Pliki nag³ówkowe biblioteki libnl.

%package static
Summary:	Static libnl library
Summary(pl):	Statyczna biblioteka libnl
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libnl library.

%description static -l pl
Statyczna biblioteka libnl.

%prep
%setup -q -n %{name}-%{version}-%{pre}
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}

%configure \
	--enable-verbose-errors

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}

%{__make} install \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_pkgconfigdir}/

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_libdir}/lib*.so.*.*-*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/netlink
%{_pkgconfigdir}/*.pc
