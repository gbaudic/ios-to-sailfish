Name:       harbour-appleseed

# >> macros
%define __provides_exclude_from ^%{_datadir}/.*$
%define __requires_exclude ^libc|python.*$
# << macros

Summary:    Migrator helper from iOS
Version:    0.1
Release:    1
License:    GPLv3+
Group:      Applications/Utility
URL:        https://github.com/gbaudic/ios-to-sailfish
Source0:    %{name}-%{version}.tar.bz2
Source1:    requirements.txt
Requires:   sailfishsilica-qt5 >= 0.10.9
Requires:   pyotherside-qml-plugin-python3-qt5 >= 1.3.0
Requires:   libsailfishapp-launcher
Requires:   python3-sqlite
Requires:   nemo-qml-plugin-dbus-qt5
Requires:   libcommhistory-qt5-tools
Requires:   nemo-qml-plugin-calendar-qt5-tools
BuildRequires:  pkgconfig(sailfishapp) >= 1.0.2
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Qml)
BuildRequires:  pkgconfig(Qt5Quick)
BuildRequires:  desktop-file-utils
BuildRequires:  python3-pip

%description
Appleseed is a migration helper to assist in importing selected contents of an iOS backup to a Sailfish device.


%prep
%setup -q -n %{name}-%{version}

%build

%qmake5 

%make_build


%install
%qmake5_install

pip3 install -r %{SOURCE1} --target=%{buildroot}%{_datadir}/%{name}/qml/pages/deps

desktop-file-install --delete-original         --dir %{buildroot}%{_datadir}/applications                %{buildroot}%{_datadir}/applications/*.desktop

%files
%defattr(-,root,root,-)
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
