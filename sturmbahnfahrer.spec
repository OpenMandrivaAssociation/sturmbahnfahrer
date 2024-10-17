%define name sturmbahnfahrer
%define oname stormbaancoureur
%define version	1.5.3
%define rel 2
%define release %mkrel %rel

Summary: Simulated obstacle course for automobiles
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://www.stolk.org/sturmbahnfahrer/download/%{oname}-%{version}.tar.bz2
Patch: sturmbahnfahrer-1.5.2-use-shared-ode.patch
Group: Games/Arcade
License: GPL
URL: https://www.sturmbahnfahrer.com/
BuildRoot: %_tmppath/%{name}-build
BuildRequires: ode-devel >= 0.6
BuildRequires: plib-devel
BuildRequires: imagemagick
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

%setup -q -n %{oname}-%{version}/src-%{oname}
%patch -p0
# x86_64
perl -pi -e "s#LIBDIRNAME=lib#LIBDIRNAME=%{_lib}#g" Makefile

# creates icons
convert -scale 16x16 images/engine.tga %{name}-16.png
convert -scale 32x32 images/engine.tga %{name}-32.png
convert -scale 48x48 images/engine.tga %{name}-48.png

%build
%make

%install
rm -rf %{buildroot}
%makeinstall DESTDIR=%{buildroot}

#icons
install -d -m 755 %{buildroot}/%{_miconsdir}
install -m 644 %{name}-16.png %{buildroot}/%{_miconsdir}/%{name}.png
install -d -m 755 %{buildroot}/%{_iconsdir}
install -m 644 %{name}-32.png %{buildroot}/%{_iconsdir}/%{name}.png
install -d -m 755 %{buildroot}/%{_liconsdir}
install -m 644 %{name}-48.png %{buildroot}/%{_liconsdir}/%{name}.png

#xdg menu
install -d -m 755 %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=Sturmbahnfahrer
Comment=Simulated obstacle course for automobiles
Exec=%{_gamesbindir}/%{oname}
Icon=%{name}
Terminal=false
Type=Application
Categories=Game;ArcageGame;
EOF

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files
%defattr(-,root,root)
%doc JOYSTICKS README TODO *.keys.example
%attr(0755,root,games) %{_gamesbindir}/*
%{_gamesdatadir}/stormbaancoureur
%{_miconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop

%clean
rm -rf $RPM_BUILD_ROOT
