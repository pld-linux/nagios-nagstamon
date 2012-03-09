Summary:	Nagios Status monitor for your Desktop
Name:		nagios-nagstamon
Version:	0.9.8
Release:	1
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://downloads.sourceforge.net/nagstamon/nagstamon_%{version}.tar.gz
# Source0-md5:	792c85018a59345625171473b39d9865
Source1:	nagstamon.desktop
URL:		http://nagstamon.ifw-dresden.de/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
# python-distribute for pkg_resources import
Requires:	python-distribute
Requires:	python-gnome-extras-egg
Requires:	python-lxml
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nagstamon is a Nagios status monitor for the desktop. It connects to
multiple Nagios, Icinga, Opsview, Centreon, Op5 Monitor/Ninja and
Check_MK Multisite monitoring servers and resides in systray or as a
floating statusbar at the desktop showing a brief summary of critical,
warning, unknown, unreachable and down hosts and services and pops up
a detailed status overview when moving the mouse pointer over it.

Connecting to displayed hosts and services is easily established by
context menu via SSH, RDP and VNC. Users can be notified by sound.
Hosts and services can be filtered by category and regular
expressions.

%prep
%setup -qc
# keep source dir versioned
mv Nagstamon .%{name}; mv .%{name}/* .

# common license
%{__rm} Nagstamon/resources/LICENSE

# win icon
%{__rm} Nagstamon/resources/nagstamon.ico

# svg used on linux, switch to .png?
# see Nagstamon/nagstamonGUI.py def CreateOutputVisuals(self): self.BitmapSuffix = ".png"
# .png used for buttons, so keep them
#rm Nagstamon/resources/*.png

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
ln $RPM_BUILD_ROOT{%{py_sitescriptdir}/Nagstamon/resources,%{_pixmapsdir}}/nagstamon.png
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/Nagstamon/resources/nagstamon.desktop
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/Nagstamon/resources/nagstamon.1
mv $RPM_BUILD_ROOT%{_bindir}/nagstamon{.py,}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYRIGHT
%attr(755,root,root) %{_bindir}/nagstamon
%{_mandir}/man1/nagstamon.1*
%{_desktopdir}/nagstamon.desktop
%{_pixmapsdir}/nagstamon.png
%dir %{py_sitescriptdir}/Nagstamon
%{py_sitescriptdir}/Nagstamon/*.py[co]
%dir %{py_sitescriptdir}/Nagstamon/resources
%{py_sitescriptdir}/Nagstamon/resources/*.ui
%{py_sitescriptdir}/Nagstamon/resources/*.svg
%{py_sitescriptdir}/Nagstamon/resources/*.png
%{py_sitescriptdir}/Nagstamon/resources/*.wav
%{py_sitescriptdir}/Nagstamon/resources/*.icns
%dir %{py_sitescriptdir}/Nagstamon/Server
%{py_sitescriptdir}/Nagstamon/Server/*.py[co]
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/nagstamon-*.egg-info
%endif
