Name:		cheat
Version:	2.5.0
Release:	1%{?dist}
Summary:	Help for various commands and their usecases

License:	MIT or GPL3	
URL:		https://github.com/chrisallenlane/cheat
Source0:	https://github.com/chrisallenlane/cheat/archive/%{version}.tar.gz	

BuildRequires:	python3-devel
Requires:	python3
Requires:	python3-docopt python3-pygments python3-termcolor

BuildArch:      noarch

%description
Cheat allows you to create and view interactive cheatsheets
on the command-line. It was designed to help remind *nix system
administrators of options for commands that they use frequently,
but not frequently enough to remember. 

%prep
%setup -q

%build
%py3_build

%install
%py3_install
mkdir -m0755 -p %{buildroot}%{_mandir}/man1
install -p -m0644 man1/cheat.1.gz %{buildroot}%{_mandir}/man1/cheat.1.gz

%files
%license LICENSE
%doc README.md CONTRIBUTING.md
%{_bindir}/cheat
%{python3_sitelib}/cheat
%{python3_sitelib}/cheat-%{version}-py%{python3_version}.egg-info
%{_datadir}/cheat
%{_sysconfdir}/cheat
%{_mandir}/man1/cheat.1*

%changelog
* Fri Feb 08 2019 Tomas Korbar <tkorbar@redhat.com> - 2.5.0-1
- Rebase to version 2.5.0

* Mon Feb 04 2019 Tomas Korbar <tkorbar@redhat.com> - 2.4.2-1
- Rebase to version 2.4.2

* Mon Jan 28 2019 Tomas Korbar <tkorbar@redhat.com> - 2.4.0-1
- Initial commit of package
