%define beta beta2

Name:		qt6-qtimageformats
Version:	6.7.0
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtbase.git
Source:		qtimageformats-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtimageformats-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{qtmajor} image formats module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6GuiTools)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	qt6-cmake
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libjpeg)
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(libmng)
BuildRequires:	pkgconfig(jasper)
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(libwebp)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glesv2)
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{qtmajor} image formats module

%package devel
Summary:	Development files for the Qt imageformats module
Requires:	%{name} = %{EVRD}
Group:		Development/C++ and C

%description devel
Development files for the Qt imageformats module

%prep
%autosetup -p1 -n qtimageformats%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON \
	-DINPUT_tiff=system \
	-DINPUT_webp=system \
	--log-level=STATUS \
|| cat CMakeFiles/CMakeOutput.log

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall

%files
# Probably not worth splitting this into many packages to avoid
# dependencies, given loads of other stuff depends on the likes
# of libpng and libwebp anyway
%{_qtdir}/plugins/imageformats

%files devel
%{_qtdir}/lib/cmake/Qt6/*.cmake
%{_qtdir}/lib/cmake/Qt6Gui/*.cmake
