Summary:	Light www browser
Name:		netsurf
Version:	2.9
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://download.netsurf-browser.org/netsurf/releases/source-full/%{name}-%{version}-full-src.tar.gz
# Source0-md5:	cfc2789997b356f2ea9d9f7694c4c909
Source1:	%{name}.desktop
Patch0:		enable-nsfb.patch
Patch1:		libnsfb-xcb-fix.patch
Patch2:		nsfb-F10-exit.patch
URL:		http://netsurf-browser.org/
BuildRequires:	SDL-devel
BuildRequires:	curl-devel
BuildRequires:	freetype-devel
BuildRequires:	libglade2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Small web browser with CSS support. NetSurf is a multi-platform
lightweight web browser. Its aim is to provide comprehensive rendering
of HTML 5 with CSS 2 in a small resource footprint while remaining
fast.

%package common
Summary:	netsurf - common files
Summary(pl.UTF-8):	netsurf - pliki wspólne
License:	GPL v2
Group:		Applications/Networking

%description common
netsurf - common files.

%description common -l pl.UTF-8
netsurf - wspólne pliki.

%package gtk
Summary:	netsurf browser gtk version
Summary(pl.UTF-8):	Wersja gtk netsurfa
License:	GPL v2
Group:		Applications/Networking
Requires:	%{name}-common = %{version}-%{release}

%description gtk
Small web browser with CSS support. NetSurf is a multi-platform
lightweight web browser. Its aim is to provide comprehensive rendering
of HTML 5 with CSS 2 in a small resource footprint while remaining
fast.

This is gtk version.

%package sdl
Summary:	netsurf browser SDL version
Summary(pl.UTF-8):	Wersja SDL netsurfa
License:	GPL v2
Group:		Applications/Networking
Requires:	%{name}-common = %{version}-%{release}

%description sdl
Small web browser with CSS support. NetSurf is a multi-platform
lightweight web browser. Its aim is to provide comprehensive rendering
of HTML 5 with CSS 2 in a small resource footprint while remaining
fast.

This is SDL version.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

cat << EOF > netsurf-2.9/Makefile.config
NETSURF_FB_FONTLIB := freetype
NETSURF_FB_FONTPATH := %{_datadir}/fonts/TTF
EOF

%build
CFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}" \
	%{__make} PREFIX=%{_prefix} \
	Q='' \
	TARGET=gtk

CFLAGS="%{rpmcflags}" LDFLAGS="%{rpmldflags}" \
	%{__make} PREFIX=%{_prefix} \
	Q='' \
	TARGET=framebuffer

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	TARGET=gtk \
	Q=''


%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX=%{_prefix} \
	TARGET=framebuffer \
	Q=''

install %{SOURCE1} $RPM_BUILD_ROOT/%{_desktopdir}
install netsurf-2.9/nsfb $RPM_BUILD_ROOT/%{_bindir}
install netsurf-2.9/nsgtk $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(644,root,root,755)
%doc netsurf-2.9/ChangeLog netsurf-2.9/README
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nsgtk
%{_desktopdir}/netsurf.desktop

%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nsfb
