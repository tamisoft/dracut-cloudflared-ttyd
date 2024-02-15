%define dracutlibdir %{_prefix}/lib/dracut
%global _missing_build_ids_terminate_build 0
Name:           dracut-cloudflared-ttyd
Version:        0.0.1
Release:        %autorelease
Summary:        Creates configuration for dracut to include a web tty and cloudflared
Group:          System
ExclusiveArch:  x86_64

Source:         dracut-cloudflared-ttyd-%{version}.tar.gz
%define         sourcename %{Source}

License:        Mixed
URL:            https://github.com/tamisoft/dracut-cloudflared-ttyd.git

BuildRequires:  wget

Requires:       dracut
Requires:       dracut-network

%description
This dracut module provides integration of the cloudflared and ttyd into the initram. This allow the user
to unlock luks encrypted devices remotely from a browser when the systemd-ask-password is prompting for it.

%prep
[ ! -e "$RPM_SOURCE_DIR" ] && mkdir -p "$RPM_SOURCE_DIR"
[ ! -e "$RPM_SOURCE_DIR/ttyd.x86_64" ] && wget -nc -q --show-progress -O "$RPM_SOURCE_DIR/ttyd.x86_64" https://github.com/tsl0922/ttyd/releases/latest/download/ttyd.x86_64
[ ! -e "$RPM_SOURCE_DIR/cloudflared-linux-amd64" ] && wget -nc -q --show-progress -O "$RPM_SOURCE_DIR/cloudflared-linux-amd64" https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
[ ! -e "$RPM_SOURCE_DIR/%{SOURCEURL0}" ] && wget -nc -q --show-progress -O "$RPM_SOURCE_DIR/%{SOURCEURL0}" https://github.com/tamisoft/dracut-cloudflared-ttyd/archive/refs/tags/%{version}.tar.gz
%setup -q

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
install -Dm755 $RPM_SOURCE_DIR/ttyd.x86_64 %{buildroot}%{_datadir}/%{name}/ttyd
%{buildroot}%{_datadir}/%{name}/ttyd --version >%{buildroot}%{_datadir}/%{name}/ttyd.version
install -Dm755 $RPM_SOURCE_DIR/cloudflared-linux-amd64 %{buildroot}%{_datadir}/%{name}/cloudflared
%{buildroot}%{_datadir}/%{name}/cloudflared version >%{buildroot}%{_datadir}/%{name}/cloudflared.version
install -Dm755 src/module-setup.sh %{buildroot}%{dracutlibdir}/modules.d/50cloudflared-ttyd/module-setup.sh
install -Dm644 src/cloudflared.service %{buildroot}%{dracutlibdir}/modules.d/50cloudflared-ttyd/cloudflared.service
install -Dm644 src/ttyd.service %{buildroot}%{dracutlibdir}/modules.d/50cloudflared-ttyd/ttyd.service
install -Dm640 src/dracut-cloudflared-ttyd %{buildroot}%{_sysconfdir}/sysconfig/dracut-cloudflared-ttyd

%files
%{_datadir}/%{name}/*
%{dracutlibdir}/modules.d/50cloudflared-ttyd/*
%config(noreplace) %{_sysconfdir}/sysconfig/dracut-cloudflared-ttyd
%license LICENSE

%changelog
* Tue Feb 13 2024 Levente Tamas
- initial release.
