#without --enable_gegl "until gegl is fast enough" as developers tell
%define with_gegl 0

Name:		darktable
Version:	1.1.3
Release:	1%{?dist}
Summary:	Utility to organize and develop raw images

Group:		Applications/Multimedia
License:	GPLv3+
URL:		http://darktable.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake
BuildRequires:	pkgconfig >= 0.22
BuildRequires:	intltool, gettext
BuildRequires:	sqlite-devel
BuildRequires:	libjpeg-devel, libpng-devel, libtiff-devel
BuildRequires:	librsvg2-devel >= 2.26
BuildRequires:	GConf2-devel, gtk2-devel, cairo-devel, libglade2-devel
BuildRequires:	lcms2-devel
BuildRequires:	exiv2-devel
BuildRequires:	lensfun-devel
BuildRequires:	GConf2
BuildRequires:	OpenEXR-devel >= 1.6
BuildRequires:	libgphoto2-devel >= 2.4.5	
BuildRequires:	libcurl-devel >= 7.18.0
BuildRequires:	flickcurl-devel
BuildRequires:	dbus-glib-devel >= 0.80 
BuildRequires:	libgnome-keyring-devel >= 2.28.0
BuildRequires:	gnome-doc-utils, fop
BuildRequires:	desktop-file-utils
BuildRequires:	SDL-devel
BuildRequires:	libsoup-devel	
%if 0%{?with_gegl}
BuildRequires:	gegl-devel
%endif

Requires:	gtk2-engines

# uses xmmintrin.h
ExclusiveArch: %{ix86} x86_64


%description
Darktable is a virtual light-table and darkroom for photographers:
it manages your digital negatives in a database and lets you view them
through a zoom-able light-table.
It also enables you to develop raw images and enhance them.


%prep
%setup -q -n %{name}-%{version}

%build
mkdir buildFedora
pushd buildFedora
%cmake \
        -DCMAKE_LIBRARY_PATH:PATH=%{_libdir} \
        -DDONT_INSTALL_GCONF_SCHEMAS:BOOLEAN=ON \
        -DUSE_GEO:BOOLEAN=ON \
        -DCMAKE_BUILD_TYPE:STRING=Release \
	-DBINARY_PACKAGE_BUILD=1 \
	-DPROJECT_VERSION:STRING="%{name}-%{version}-%{release}" \
	.. 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
pushd buildFedora
make install DESTDIR=$RPM_BUILD_ROOT
popd
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
%find_lang %{name}
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/darktable


%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
update-desktop-database &> /dev/null || :                                       
if [ $1 -eq 0 ] ; then                                                          
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null                     
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :            
fi                                                                              

%posttrans                                                                      
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%preun
 
%files -f %{name}.lang 
%defattr(-,root,root,-)
%doc doc/README doc/AUTHORS doc/LICENSE doc/TRANSLATORS
%{_bindir}/darktable
%{_bindir}/darktable-cli
%{_bindir}/darktable-cltest
%{_bindir}/darktable-viewer
%{_libdir}/darktable
%{_datadir}/applications/darktable.desktop
%{_datadir}/darktable
%{_datadir}/icons/hicolor/*/apps/darktable.*
%{_datadir}/man/man1/darktable.1.gz


%changelog
* Mon Feb 11 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.3-1
- Upgrade to 1.1.3

* Fri Feb  1 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.2+26~ge1f2980
- Pre 1.1.3

* Mon Jan 21 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.2-2
- Add missing gtk2-engine dependancy (bug #902288)

* Sat Jan 12 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.2-1
- Upgrade to 1.1.2

* Sun Jan  6 2013 Edouard Bourguignon <madko@linuxed.net> - 1.1.1-2
- Add map mode

* Wed Nov 28 2012 Edouard Bourguignon <madko@linuxed.net> - 1.1.1-1
- Upgrade to 1.1.1 

* Sat Nov 24 2012 Edouard Bourguignon <madko@linuxed.net> - 1.1-1
- Upgrade to 1.1

* Wed Nov 14 2012 Edouard Bourguignon <madko@linuxed.net> - 1.1-0.1.rc2
- Upgrade to 1.1~rc2

* Wed Oct 31 2012 Edouard Bourguignon <madko@linuxed.net> - 1.1-0.1.rc1
- Upgrade to 1.1~rc1

* Thu Jul 26 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0.5-1
- Upgrade to 1.0.5

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 15 2012 Jindrich Novy <jnovy@redhat.com> - 1.0.4-2
- rebuild because of new libgphoto2

* Sat Jun 30 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0.4-1
- Upgrade to 1.0.4

* Sun Apr 29 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0.3-1
- Upgrade to 1.0.3

* Sat Apr 28 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0.1-1
- Upgrade to 1.0.1

* Thu Mar 15 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-1
- Upgrade to stable 1.0

* Sun Mar 11 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.4.rc2
- Remove pre script

* Sat Mar 10 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.3.rc2
- Patch for uninitialised variables

* Sat Mar 10 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.2.rc2
- Remove useless darktable gconf schemas

* Sat Mar 10 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.1.rc2
- Upgrade to rc2

* Wed Mar  7 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.2.rc1
- Correct invalid type in darktable gconf schemas

* Sun Mar  4 2012 Edouard Bourguignon <madko@linuxed.net> - 1.0-0.1.rc1
- Darktable 1.0 RC1

* Mon Dec  5 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9.3-2
- Add SDL-devel for darktable-viewer

* Mon Nov  7 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9.3-1
- Upgrade to 0.9.3

* Fri Oct 14 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.9.2-2
- rebuild (exiv2)

* Fri Aug 26 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9.2-1
- Upgrade to 0.9.2

* Thu Jul 28 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9.1-1
- Upgrade to 0.9.1
- Remove some old patches

* Sat Jul  2 2011 Edouard Bourguignon <madko@linuxed.net> - 0.9-1
- Upgrade to 0.9

* Mon May 23 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-11
- Add a patch for BINARY_PACKAGE_BUILD (preventing march=native)

* Fri Apr 22 2011 Dan Horák <dan[at]danny.cz> - 0.8-10
- make it x86-only

* Fri Apr 22 2011 Dan Horák <dan[at]danny.cz> - 0.8-9
- don't use x86-only compiler flags on non-x86 arches

* Tue Apr 19 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-8
- Change build option

* Mon Apr 11 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.8-7.1
- rebuild (exiv2)

* Wed Mar 30 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-7
- Change cmake options

* Tue Mar 22 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-6
- Keep rpath for internal libs 

* Wed Feb 23 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-5
- Change build options
- Change permission on gconf darktable.schemas
- Add patch and cmake option to remove relative path (thanks to Karl Mikaelsson)

* Sat Feb 19 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-4
- Add missing doc files

* Sat Feb 19 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-3
- Clean up set but unused variables patch for GCC 4.6 (Karl Mikaelsson)

* Thu Feb 17 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-2
- Add flickcurl support
- Add patch to fix unused but set variables

* Tue Feb 15 2011 Edouard Bourguignon <madko@linuxed.net> - 0.8-1
- Upgrade to version 0.8
- Rebuilt using cmake

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 03 2011 Edouard Bourguignon <madko@linuxed.net> - 0.7.1-3
- Change exiv2 headers to use the new umbrella header (#666887)

* Sat Jan 01 2011 Rex Dieter <rdieter@fedoraproject.org> - 0.7.1-2
- rebuild (exiv2)

* Tue Dec 14 2010 Edouard Bourguignon <madko@linuxed.net> - 0.7.1-1
- Upgrade to version 0.7.1

* Mon Nov 29 2010 Edouard Bourguignon <madko@linuxed.net> - 0.7-1
- Upgrade to darktable 0.7

* Mon Sep 20 2010 Edouard Bourguignon <madko@linuxed.net> - 0.6-9
- Only use RPM_BUILD_ROOT
- Remove duplicated doc

* Mon Sep 20 2010 Edouard Bourguignon <madko@linuxed.net> - 0.6-8
- Change gegl-devel buildrequires
- Correct with_gegl option
- Correct typo in changelog
- Remove useless configure option (--disable-schemas)
- Add buildrequires on pkgconfig

* Fri Sep 10 2010 Edouard Bourguignon <madko@linuxed.net> - 0.6-7
- Remove useless removal of *.a files
- Change name of desktop patch (no version)

* Tue Aug 31 2010 Dmitrij S. Kryzhevich <krege@land.ru> - 0.6-6
- disable static lib and schemas
- update desktop database and icon cache
- disable gegl support 

* Mon Aug 30 2010 Edouard Bourguignon <madko@linuxed.net> - 0.6-5
- Upgrade to Darktable 0.6
- Change to tar.gz for source0
- Remove rpath patch
- Add BuildRequires on missing devel packages
- Change path to libdarktable.so
- Add icons
- Make a clean desktop file
- Add desktop file validation

* Mon Aug 23 2010 Edouard Bourguignon <madko@linuxed.net> - 0.5-4
- Use Gconf scriplets to hangle gconf schema
- Add a patch to remove rpath from Dmitrij S. Kryzhevich

* Wed Jul  7 2010 Edouard Bourguignon <madko@linuxed.net> - 0.5-3
- Removing rpath

* Fri Apr 23 2010 Edouard Bourguignon <madko@linuxed.net> - 0.5-2
- Update to 0.5
- Shorten file list
- Use devel packages for building
- Correct URL for Source0

* Tue Feb 02 2010 İbrahim Eser <ibrahimeser@gmx.com.tr> - 0.4-1
- Initial package.
