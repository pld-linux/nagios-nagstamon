Summary:	Nagios Status monitor for your Desktop
Name:		nagios-nagstamon
Version:	0.9.4
Release:	0.9
License:	GPL v2
Group:		X11/Applications/Networking
Source0:	http://downloads.sourceforge.net/nagstamon/nagstamon_%{version}.tar.gz
# Source0-md5:	52cd8bfc28086e29a84eccb607e9ce3c
Source1:	nagstamon.desktop
# Source1-md5:	bf06c260f3ace25a415927bc1aac9914
URL:		http://nagstamon.sourceforge.net/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
# for pkg_resources import
Requires:	python-distribute
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nagstamon is a Nagios status monitor for the desktop. It connects to
multiple Nagios, Icinga, Opsview and Centreon monitoring servers and
resides in systray or as a floating statusbar at the desktop showing a
brief summary of critical, warning, unknown, unreachable and down
hosts and services and pops up a detailed status overview when moving
the mouse pointer over it.

Connecting to displayed hosts and services is easily established by
context menu via SSH, RDP and VNC. Users can be notified by sound.
Hosts and Services can be filtered by category and regular
expressions.

%prep
%setup -q -n nagstamon_%{version}

# common license
rm Nagstamon/resources/LICENSE

# win icon
rm Nagstamon/resources/nagstamon.ico

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
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
ln $RPM_BUILD_ROOT{%{py_sitescriptdir}/Nagstamon/resources,%{_pixmapsdir}}/nagstamon.png
rm $RPM_BUILD_ROOT%{py_sitescriptdir}/Nagstamon/resources/nagstamon.1

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog COPYRIGHT
%attr(755,root,root) %{_bindir}/nagstamon
%{_mandir}/man1/nagstamon.1*
%{_desktopdir}/nagstamon.desktop
/usr/share/pixmaps/nagstamon.png
%dir %{py_sitescriptdir}/Nagstamon
%{py_sitescriptdir}/Nagstamon/*.py[co]
%dir %{py_sitescriptdir}/Nagstamon/resources
%{py_sitescriptdir}/Nagstamon/resources/*.glade
%{py_sitescriptdir}/Nagstamon/resources/*.svg
%{py_sitescriptdir}/Nagstamon/resources/*.png
%{py_sitescriptdir}/Nagstamon/resources/*.wav
%if "%{py_ver}" > "2.4"
%{py_sitescriptdir}/nagstamon-*.egg-info
%endif
