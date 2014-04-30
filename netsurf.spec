Summary:	Light WWW browser
Name:		netsurf
Version:	3.1
Release:	1
License:	GPL v2
Group:		Applications/Networking
Source0:	http://download.netsurf-browser.org/netsurf/releases/source/%{name}-%{version}-src.tar.gz
# Source0-md5:	b83932b311716054a5189f121cdd5fd4
Source1:	%{name}.desktop
Patch0:		nsfb-ldflags.patch
URL:		http://netsurf-browser.org/
BuildRequires:	SDL-devel
BuildRequires:	curl-devel
BuildRequires:	freetype-devel
BuildRequires:	libCSS-devel >= 0.3.0
BuildRequires:	libdom-devel >= 0.1.0
BuildRequires:	libglade2-devel
BuildRequires:	libhubbub-devel >= 0.3.0
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel
BuildRequires:	libnsbmp-devel >= 0.1.1
BuildRequires:	libnsfb-devel >= 0.1.1
BuildRequires:	libnsgif-devel >= 0.1.1
BuildRequires:	libparserutils-devel >= 0.2.0
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	libsvgtiny-devel >= 0.1.1
BuildRequires:	libwapcaplet-devel >= 0.2.1
BuildRequires:	netsurf-buildsystem >= 1.1
BuildRequires:	nsgenbind >= 0.1.0
BuildRequires:	perl-HTML-Parser
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
Group:		Applications/Networking

%description common
netsurf - common files.

%description common -l pl.UTF-8
netsurf - wspólne pliki.

%package gtk
Summary:	Netsurf browser GTK version
Summary(pl.UTF-8):	Wersja gtk netsurfa
Group:		Applications/Networking
Requires:	%{name}-common = %{version}-%{release}

%description gtk
Small web browser with CSS support. NetSurf is a multi-platform
lightweight web browser. Its aim is to provide comprehensive rendering
of HTML 5 with CSS 2 in a small resource footprint while remaining
fast.

This is GTK version.

%package sdl
Summary:	netsurf browser SDL version
Summary(pl.UTF-8):	Wersja SDL netsurfa
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

cat << EOF > Makefile.config
NETSURF_FB_FONTLIB := freetype
NETSURF_FB_FONTPATH := %{_datadir}/fonts/TTF
EOF

%build
export CC="%{__cc}"
# while cxx not needed, somewhy it helps race condition on carme build
export CXX="%{__cxx}"
# silence -Werror:
#src/surface/vnc.c: In function 'vnc_input':
#src/surface/vnc.c:489:9: error: variable 'ret' set but not used [-Werror=unused-but-set-variable]
export CFLAGS="%{rpmcflags} -Wno-error=unused-but-set-variable"
export LDFLAGS="%{rpmldflags}"

# make -j1 or it won't find libwapcaplet/libwapcaplet.h

%{__make} -j1 \
	PREFIX=%{_prefix} \
	Q='' \
	TARGET=gtk

%{__make} -j1 \
	PREFIX=%{_prefix} \
	Q='' \
	TARGET=framebuffer

%install
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	Q='' \
	PREFIX=%{_prefix} \
	TARGET=gtk \
	DESTDIR=$RPM_BUILD_ROOT


%{__make} install \
	Q='' \
	PREFIX=%{_prefix} \
	TARGET=framebuffer \
	DESTDIR=$RPM_BUILD_ROOT

# this is binary from last "make install", we install more specific binary ourself
%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/netsurf

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install nsfb $RPM_BUILD_ROOT/%{_bindir}
install nsgtk $RPM_BUILD_ROOT/%{_bindir}

%clean
rm -rf $RPM_BUILD_ROOT

%files common
%defattr(644,root,root,755)
%doc README
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nsgtk
%{_desktopdir}/netsurf.desktop

%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/nsfb
