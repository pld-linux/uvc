#
# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_with	verbose		# verbose build (V=1)
#
%define		subver	215
%define		pname	uvc
#
Summary:	USB Video Class driver
Summary(pl.UTF-8):	Sterownik USB Video Class
Name:		%{pname}%{_alt_kernel}
Version:	0.%{subver}.1
Release:	8
License:	GPL v2
Group:		Base/Kernel
#Source0:	http://www.lavrsen.dk/twiki/pub/Motion/VideoFourLinuxLoopbackDevice/%{pname}-%{version}.tar.gz
Source0:	%{pname}-r%{subver}.tar.gz
# Source0-md5:	96c35fcec98f1549fb47a3a456c234b4
Patch0:		%{pname}-driver.patch
URL:		http://linux-uvc.berlios.de/
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
USB Video Class (uvc) driver.

%description -l pl.UTF-8
Sterownik USB Video Class.

%package -n kernel%{_alt_kernel}-misc-uvc
Summary:	uvc kernel module
Summary(pl.UTF-8):	uvc
Release:	%{subver}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-uvc
USB Video Class (uvc) linux kernel modul.

%description -n kernel%{_alt_kernel}-misc-uvc -l pl.UTF-8
Moduł jądra linuksa dla USB Video Class.

%prep
%setup -q -n %{pname}-r%{subver}
%patch0 -p0

%build
%build_kernel_modules -m %{pname}video

%install
rm -rf $RPM_BUILD_ROOT
%install_kernel_modules -m %{pname}video -d kernel/drivers/misc

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-uvc
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-uvc
%depmod %{_kernel_ver}

%files -n kernel%{_alt_kernel}-misc-uvc
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/misc/%{pname}video.ko*
