%global checkout 20111212gitb6b1de3

Name:           HeeksCAD
Version:        0.18.0
Release:        0.1.%{checkout}%{?dist}
Summary:        CAD application using OpenCASDADE and wxWidgets
Group:          Applications/Engineering
License:        BSD
URL:            https://github.com/Heeks/heekscad
#fedora-getsvn HeeksCAD https://github.com/Heeks/heekscad.git/trunk HEAD
Source0:        %{name}-svnHEAD.tar.bz2
Patch0:         cmake.patch


BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  gettext
BuildRequires:  OCE-devel
BuildRequires:  python-devel
#BuildRequires:  tinyxml-devel
BuildRequires:  wxGTK-devel


%description
Functionality: Import solid models from STEP and IGES files. Draw construction
geometry and lines and arcs. Create new primitive solids, or make solids by
extruding a sketch or by making a lofted solid between sketches. Modify solids
using blending, or boolean operations. Save IGES, STEP and STL. Printer plot
the 2D geometry or to HPGL. Import and export dxf files; lines, arcs, ellipses,
splines and polylines are supported. Use the geometric constraints solver to
create accurate drawings from rough sketches.


%package devel
Summary:    Libraries and header files for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package provides the libraries, include files, and other
resources needed for developing %{name} plugins.


%prep
%setup -q -n %{name}
%patch0 -p1 -b .cmake-build

# fix permissions on source files
chmod a-x src/*
chmod a-x tinyxml/*

# fix EOLs
sed -i 's/\r//' HeeksCAD.desktop


%build
%{cmake} .
make %{?_smp_mflags} CFLAGS="%{optflags}"


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mv -f %{buildroot}%{_bindir}/heekscad-%{version} %{buildroot}%{_bindir}/heekscad


for dir in PyHeeksCAD interface src tinyxml unittest sketchsolve/src
do
   install -d  %{buildroot}%{_includedir}/%{name}/$dir
   find $dir -maxdepth 1 \( -name "*.h" -o -name "*.cpp" \) -exec cp {} %{buildroot}%{_includedir}/%{name}/$dir/ \;;
done


desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%find_lang %{name}




%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc COPYING docs/Manual
%{_bindir}/heekscad
%{_datadir}/heekscad
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/scalable/apps/*

%files devel
%doc
%{_includedir}/%{name}


%changelog
* Mon Dec 12 2011 Chris Spike <spike@fedoraproject.org> 0.18.0-0.1.20111212gitb6b1de3
- 