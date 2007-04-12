%define name sturmbahnfahrer
%define version	1.3
%define rel 1
%define release %mkrel %rel

Summary: Simulated obstacle course for automobiles
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://www.stolk.org/sturmbahnfahrer/download/%{name}-%{version}.tar.bz2
Group: Games/Arcade
License: GPL
URL: http://www.sturmbahnfahrer.com/
BuildRoot: %_tmppath/%{name}-build
BuildRequires: ode-devel >= 0.6
BuildRequires: plib-devel
BuildRequires: ImageMagick
BuildRequires: mesaglut-devel
BuildRequires: alsa-lib-devel

%description
Sturmbahnfahrer... for expert drivers only.
If you want to master it, try to have the laws of physics work with you, not 
against you.

Enabling technologies behind Sturmbahnfahrer include the Open Dynamics Engine 
and the portable game library known as PLIB.

Sturmbahnfahrer is a game by Bram Stolk.

%prep

%setup -q
# use shared ode
perl -pi -e "s#\Q\$(ODEPREFIX)/lib/libode.a\E#-lode#" Makefile
# x86_64
perl -pi -e "s#/lib#/%{_lib}#g" Makefile

# creates icons
convert -scale 16x16 images/engine.tga %{name}-16.png
convert -scale 32x32 images/engine.tga %{name}-32.png
convert -scale 48x48 images/engine.tga %{name}-48.png

%build
%make

%install
rm -rf %{buildroot}
install -d -m 755 %{buildroot}%{_gamesbindir}
install -d -m 755 %{buildroot}%{_gamesdatadir}/%{name}/images
install -d -m 755 %{buildroot}%{_gamesdatadir}/%{name}/sounds
install -d -m 755 %{buildroot}%{_gamesdatadir}/%{name}/models
%makeinstall DESTDIR=%{buildroot}

#icons
install -d -m 755 %{buildroot}/%{_miconsdir}
install -m 644 %{name}-16.png %{buildroot}/%{_miconsdir}/%{name}.png
install -d -m 755 %{buildroot}/%{_iconsdir}
install -m 644 %{name}-32.png %{buildroot}/%{_iconsdir}/%{name}.png
install -d -m 755 %{buildroot}/%{_liconsdir}
install -m 644 %{name}-48.png %{buildroot}/%{_liconsdir}/%{name}.png

#old debian-type menu
install -d -m 755 %{buildroot}%{_menudir}
cat > %{buildroot}%{_menudir}/%{name} << EOF
?package(%name): needs="x11" \
section="More Applications/Games/Arcade" \
title="Sturmbahnfahrer" \
longtitle="%{Summary}" \
command="%{_gamesbindir}/%{name}" \
icon="%{name}.png" \
xdg="true"
EOF

#xdg menu
install -d -m 755 %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Sturmbahnfahrer
Comment=%{Summary}
Exec=%{_gamesbindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcageGame;X-MandrivaLinux-MoreApplications-Games-Arcade;
EOF

%post
%{update_menus}

%postun
%{clean_menus}

%files
%defattr(-,root,root)
%doc JOYSTICKS README TODO sturmbahnfahrer.keys.example
%attr(0755,root,games) %{_gamesbindir}/%{name}
%{_gamesdatadir}/%{name}
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_menudir}/%{name}
%{_datadir}/applications/mandriva-%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT



