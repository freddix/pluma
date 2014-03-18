Summary:	MATE text editor
Name:		pluma
Version:	1.8.0
Release:	1
License:	GPL v2
Group:		X11/Applications/Editors
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	cdebd8c3e32bb4624354f2b435fecc23
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	enchant-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	gtksourceview2-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Provides:	mate-text-editor = %{version}-%{release}
Obsoletes:	mate-text-editor <= %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
Pluma is a small but powerful text editor for GTK+ and/or MATE. It
includes such features as split-screen mode, a plugin API, which
allows Pluma to be extended to support many features while remaining
small at its core, multiple document editing and many more functions.

%package devel
Summary:	Pluma header files
Group:		X11/Development/Libraries
# don't require base
Provides:	mate-text-editor-devel = %{version}-%{release}
Obsoletes:	mate-text-editor-devel <= %{version}-%{release}

%description devel
Pluma header files

%package apidocs
Summary:	Pluma API documentation
Group:		Documentation
Requires:	gtk-doc-common
Provides:	mate-text-editor-apidocs = %{version}-%{release}
Obsoletes:	mate-text-editor-apidocs <= %{version}-%{release}

%description apidocs
Pluma API documentation.

%prep
%setup -q

# kill mate common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__libtoolize}
%{__intltoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
%configure \
	--disable-python		\
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/pluma/*/*.la
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/pluma.convert
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/{ca@valencia,crh,en@shaw,la}

%find_lang pluma --with-mate --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_gsettings_cache

%postun
%update_desktop_database
%update_gsettings_cache

%files -f pluma.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS

# dirs
%dir %{_libdir}/pluma
%dir %{_libdir}/pluma/plugins
%dir %{_libdir}/pluma/plugin-loaders

%attr(755,root,root) %{_bindir}/pluma
%attr(755,root,root) %{_libdir}/pluma/plugins/*.so
%attr(755,root,root) %{_libdir}/pluma/plugin-loaders/libcloader.so
%{_libdir}/pluma/plugins/*.pluma-plugin

%{_datadir}/pluma
%{_datadir}/glib-2.0/schemas/org.mate.*.gschema.xml

%{_desktopdir}/pluma.desktop
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/pluma
%{_pkgconfigdir}/pluma.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/pluma

