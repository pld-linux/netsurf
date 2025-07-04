#
# Conditional build:
%bcond_with	gstreamer	# GStreamer-based video support
%bcond_without	js		# JavaScript support
%bcond_without	libjxl		# JPEG-XL image support via libjxl
%bcond_with	pdf		# PDF export and GTK+ printing support via libharu [needs update?]
%bcond_without	webp		# WebP image support
#
Summary:	Light WWW browser with CSS support
Summary(pl.UTF-8):	Lekka przeglądarka WWW z obsługą CSS
Name:		netsurf
Version:	3.11
Release:	4
License:	GPL v2 with OpenSSL exception (code), MIT (artwork)
Group:		Applications/Networking
Source0:	http://download.netsurf-browser.org/netsurf/releases/source/%{name}-%{version}-src.tar.gz
# Source0-md5:	d4a8c61cea7d507aa6633f4ab99980c9
Source1:	%{name}.desktop
Patch0:		nsfb-ldflags.patch
Patch1:		%{name}-link.patch
Patch3:		optflags.patch
Patch4:		fixes.patch
Patch5:		%{name}-utf8proc.patch
URL:		http://netsurf-browser.org/
BuildRequires:	curl-devel
BuildRequires:	freetype-devel >= 2
%{?with_gstreamer:BuildRequires:	gstreamer0.10-devel >= 0.10}
BuildRequires:	gtk+2-devel >= 2.0
BuildRequires:	libCSS-devel >= 0.9.2
BuildRequires:	libdom-devel >= 0.4.2
%{?with_pdf:BuildRequires:	libharu-devel}
BuildRequires:	libhubbub-devel >= 0.3.8
%{?with_libjxl:BuildRequires:	libjxl-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libnsbmp-devel >= 0.1.7
BuildRequires:	libnsfb-devel >= 0.2.2
BuildRequires:	libnsgif-devel >= 1.0.0
BuildRequires:	libnslog-devel >= 0.1.3
BuildRequires:	libnspsl-devel >= 0.1.7
BuildRequires:	libnsutils-devel >= 0.1.1
BuildRequires:	libparserutils-devel >= 0.2.5
BuildRequires:	libpng-devel
BuildRequires:	librsvg-devel
BuildRequires:	libsvgtiny-devel >= 0.1.8
BuildRequires:	libwapcaplet-devel >= 0.4.3
%{?with_webp:BuildRequires:	libwebp-devel}
BuildRequires:	openssl-devel
BuildRequires:	netsurf-buildsystem >= 1.10
BuildRequires:	nsgenbind >= 0.9
BuildRequires:	perl-HTML-Parser
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	utf8proc-devel >= 2.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NetSurf is a multi-platform lightweight web browser. Its aim is to
provide comprehensive rendering of HTML 5 with CSS 2 in a small
resource footprint while remaining fast.

%description -l pl.UTF-8
NetSurf to wieloplatformowa, lekka przeglądarka WWW. Celem jest
zapewnienie kompletnego renderowania HTML 5 z CSS 2 przy małym
wykorzystanie zasobów, z zachowaniem dużej szybkości.

%package common
Summary:	NetSurf - common files
Summary(pl.UTF-8):	NetSurf - pliki wspólne
Group:		Applications/Networking

%description common
NetSurf - common files.

%description common -l pl.UTF-8
NetSurf - wspólne pliki.

%package gtk
Summary:	NetSurf web browser - GTK+ version
Summary(pl.UTF-8):	Wersja GTK+ przeglądarki WWW NetSurf
Group:		Applications/Networking
Requires(post,postun):	desktop-file-utils
Requires:	%{name}-common = %{version}-%{release}
Requires:	libCSS >= 0.9.2
Requires:	libdom >= 0.4.2
Requires:	libhubbub >= 0.3.8
Requires:	libnsbmp >= 0.1.7
Requires:	libnsgif >= 1.0.0
Requires:	libnspsl >= 0.1.7
Requires:	libparserutils >= 0.2.5
Requires:	libsvgtiny >= 0.1.8
Requires:	libwapcaplet >= 0.4.3
Requires:	utf8proc >= 2.4.0

%description gtk
NetSurf is a multi-platform lightweight web browser. Its aim is to
provide comprehensive rendering of HTML 5 with CSS 2 in a small
resource footprint while remaining fast.

This package contains GTK+ version.

%description gtk -l pl.UTF-8
NetSurf to wieloplatformowa, lekka przeglądarka WWW. Celem jest
zapewnienie kompletnego renderowania HTML 5 z CSS 2 przy małym
wykorzystanie zasobów, z zachowaniem dużej szybkości.

Ten pakiet zawiera wersję GTK+.

%package sdl
Summary:	NetSurf web browser - SDL (framebuffer aware) version
Summary(pl.UTF-8):	Wersja SDL (obsługująca framebuffer) przeglądarki WWW NetSurf
Group:		Applications/Networking
Requires:	%{name}-common = %{version}-%{release}
Requires:	libCSS >= 0.9.2
Requires:	libdom >= 0.4.2
Requires:	libhubbub >= 0.3.8
Requires:	libnsbmp >= 0.1.7
Requires:	libnsfb >= 0.2.2
Requires:	libnsgif >= 1.0.0
Requires:	libnspsl >= 0.1.7
Requires:	libparserutils >= 0.2.5
Requires:	libsvgtiny >= 0.1.8
Requires:	libwapcaplet >= 0.4.3
Requires:	utf8proc >= 2.4.0
Suggests:	fonts-TTF-DejaVu

%description sdl
NetSurf is a multi-platform lightweight web browser. Its aim is to
provide comprehensive rendering of HTML 5 with CSS 2 in a small
resource footprint while remaining fast.

This package contains SDL, framebuffer aware version.

%description sdl -l pl.UTF-8
NetSurf to wieloplatformowa, lekka przeglądarka WWW. Celem jest
zapewnienie kompletnego renderowania HTML 5 z CSS 2 przy małym
wykorzystanie zasobów, z zachowaniem dużej szybkości.

Ten pakiet zawiera wersję SDL, obsługującą framebuffer.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1

cat << EOF > Makefile.config
NETSURF_FB_FONTLIB := freetype
NETSURF_FB_FONTPATH := %{_datadir}/fonts/TTF
NETSURF_USE_NSSVG := YES
NETSURF_USE_RSVG := YES
%{?with_webp:NETSURF_USE_WEBP := YES}
%{?with_gstreamer:NETSURF_USE_VIDEO := YES}
%{?with_pdf:NETSURF_USE_HARU_PDF := YES}
%{!?with_libjxl:NETSURF_USE_JPEGXL := NO}
EOF

%if %{with gstreamer}
# GStreamer 0.10 uses now deprecated glib mutex APIs
%{__sed} -i -e '/-DG_DISABLE_DEPRECATED/d' frontends/gtk/Makefile
%endif
# gdk-pixbuf 2.31 deprecates GdkPixdata
%{__sed} -i -e '/-DGDK_PIXBUF_DISABLE_DEPRECATED/d' frontends/gtk/Makefile

%build
export CC="%{__cc}"
# while cxx not needed, somewhy it helps race condition on carme build
export CXX="%{__cxx}"
# silence -Werror:
#src/surface/vnc.c: In function 'vnc_input':
#src/surface/vnc.c:489:9: error: variable 'ret' set but not used [-Werror=unused-but-set-variable]
export CFLAGS="%{rpmcflags} -Wno-error=unused-but-set-variable -D_GNU_SOURCE"
export CXXFLAGS="%{rpmcxxflags} -Wno-error=unused-but-set-variable -D_GNU_SOURCE"
export LDFLAGS="%{rpmldflags}"

# make -j1 or it won't find libwapcaplet/libwapcaplet.h

%{__make} \
	OPTFLAGS="%{rpmcflags} -Wno-error=unused-but-set-variable -D_GNU_SOURCE" \
	OPTLDFLAGS="%{rpmldflags}" \
	PREFIX=%{_prefix} \
	Q='' \
	TARGET=gtk2

%{__make} \
	OPTFLAGS="%{rpmcflags} -Wno-error=unused-but-set-variable -D_GNU_SOURCE" \
	OPTLDFLAGS="%{rpmldflags}" \
	PREFIX=%{_prefix} \
	Q='' \
	TARGET=framebuffer

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	Q='' \
	PREFIX=%{_prefix} \
	TARGET=gtk2 \
	DESTDIR=$RPM_BUILD_ROOT


%{__make} install \
	Q='' \
	PREFIX=%{_prefix} \
	TARGET=framebuffer \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}

# compatibility with older PLD packages
ln -sf netsurf-fb $RPM_BUILD_ROOT%{_bindir}/nsfb
ln -sf netsurf-gtk2 $RPM_BUILD_ROOT%{_bindir}/nsgtk

%clean
rm -rf $RPM_BUILD_ROOT

%post gtk
%update_desktop_database_post

%postun gtk
%update_desktop_database_postun

%files common
%defattr(644,root,root,755)
%doc COPYING
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/Messages
%{_datadir}/%{name}/SearchEngines
%{_datadir}/%{name}/default.ico
%{_datadir}/%{name}/languages
%{_datadir}/%{name}/*.css
%{_datadir}/%{name}/*.html
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.txt
%{_datadir}/%{name}/*.ui
%{_datadir}/%{name}/*.xpm
%{_datadir}/%{name}/icons
%{_datadir}/%{name}/throbber
%lang(de) %{_datadir}/%{name}/de
%{_datadir}/%{name}/en
%lang(fr) %{_datadir}/%{name}/fr
%lang(it) %{_datadir}/%{name}/it
%lang(ja) %{_datadir}/%{name}/ja
%lang(nl) %{_datadir}/%{name}/nl
%lang(zh_CN) %{_datadir}/%{name}/zh_CN

%files gtk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/netsurf-gtk2
%attr(755,root,root) %{_bindir}/nsgtk
%{_desktopdir}/netsurf.desktop

%files sdl
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/netsurf-fb
%attr(755,root,root) %{_bindir}/nsfb
