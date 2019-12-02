%global sheets_commit 3b5f3db283020f9e601da69f7722db7a53625744
%global sheets_commit_short 3b5f3db

# https://github.com/cheat/cheat
%global goipath         github.com/cheat/cheat
Version:                3.2.1
%global tag             3.2.1

%gometa

%global common_description %{expand:
Cheat allows you to create and view interactive cheatsheets on the command-
line. It was designed to help remind *nix system administrators of options for
commands that they use frequently, but not frequently enough to remember.}

%global golicenses      LICENSE.txt
%global godocs          README.md CONTRIBUTING.md cmd/cheat/docopt.txt

Name:           cheat
Release:        1%{?dist}
Summary:        Help for various commands and their use cases

License:        MIT
URL:            %{gourl}
Source0:        %{gosource}
Source1:        https://github.com/cheat/cheatsheets/archive/3b5f3db.tar.gz#/cheatsheets.tar.gz
Source2:        cheat-config-FEDORA.yml

BuildRequires:  golang(github.com/alecthomas/chroma/quick)
BuildRequires:  golang(github.com/docopt/docopt-go)
BuildRequires:  golang(github.com/mattn/go-isatty)
BuildRequires:  golang(github.com/mgutz/ansi)
BuildRequires:  golang(github.com/mitchellh/go-homedir)
BuildRequires:  golang(gopkg.in/yaml.v2)
BuildRequires:  golang(gopkg.in/yaml.v1)
BuildRequires:  golang(github.com/davecgh/go-spew/spew)

Requires:       fzf
Recommends:     cheat-community-cheatsheets

%description
%{common_description}

%package bash-completion
Summary: Bash completion support for %{name}
BuildArch: noarch
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: bash bash-completion

%description bash-completion
Files needed to support bash completion.

%package fish-completion
Summary: Fish completion support for %{name}
BuildArch: noarch
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: fish

%description fish-completion
Files needed to support fish completion.

%package community-cheatsheets
Summary:   Cheatsheets created by comunity for %{name}
URL:       https://github.com/cheat/cheatsheets
BuildArch: noarch
Requires:  %{name}%{?_isa} = %{version}-%{release}
Supplements:  cheat

%description community-cheatsheets
Cheatsheets for various programs created and maintained by the
community.

%gopkg

%prep
%goprep
tar -xf %{SOURCE1}

%build
for cmd in cmd/* ; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
%gopkginstall
mkdir -m 0755 -p                            %{buildroot}%{_datadir}/bash-completion/completions
mkdir -m 0755 -p                            %{buildroot}%{_datadir}/fish/vendor_completions.d

install -m 0644 -p scripts/cheat-autocompletion.bash %{buildroot}%{_datadir}/bash-completion/completions/cheat
install -m 0644 -p scripts/cheat-autocompletion.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/cheat.fish

install -m 0755 -vd                         %{buildroot}%{_bindir}
install -m 0755 -vp %{gobuilddir}/bin/cheat %{buildroot}%{_bindir}/

# Install cheatsheets
rm -rf /cheatsheets/.github

mkdir -m 0755 -p %{buildroot}/%{_datadir}/cheat

for sheet in cheatsheets-%{sheets_commit}/* ; do
  install -m 0644 -p $sheet %{buildroot}/%{_datadir}/cheat/
done

mkdir -m 0755 -p %{buildroot}%{_sysconfdir}/profile.d
mkdir -m 0755 -p %{buildroot}%{_sysconfdir}/cheat
install -m 0644 -p scripts/fzf.bash %{buildroot}%{_sysconfdir}/profile.d/cheat.sh
install -m 0644 -p %{SOURCE2} %{buildroot}%{_sysconfdir}/cheat/conf.yml

%check
%gocheck

%files
%license LICENSE.txt
%doc README.md CONTRIBUTING.md cmd/cheat/docopt.txt
%{_bindir}/cheat
%config(noreplace) %{_sysconfdir}/profile.d/cheat.sh

%files community-cheatsheets
%dir %{_sysconfdir}/cheat
%config(noreplace) %{_sysconfdir}/cheat/conf.yml
%dir %{_datadir}/cheat
%{_datadir}/cheat/*

%files bash-completion
%{_datadir}/bash-completion/completions/cheat

%files fish-completion
%{_datadir}/fish/vendor_completions.d/cheat.fish

%gopkgfiles

%changelog
* Wed Oct 30 11:56:04 CET 2019 Tomas Korbar <tkorbar@redhat.com> - 3.2.1-1
- Initial package
