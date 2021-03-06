Name:           xenopsd
Version:        0.12.0
Release:        1%{?dist}
Summary:        Simple VM manager
License:        LGPL
URL:            https://github.com/xapi-project/xenopsd
Source0:        https://github.com/xapi-project/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        xenopsd-xc-init
Source2:        xenopsd-simulator-init
Source4:        xenopsd-xenlight-init
Source5:        make-xsc-xenopsd.conf
Source6:        xenopsd-network-conf
Source7:        xenopsd-vncterm-wrapper
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-findlib-devel
BuildRequires:  ocaml-rpc-devel
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  ocaml-cmdliner-devel
BuildRequires:  ocaml-cohttp-devel
BuildRequires:  forkexecd-devel
BuildRequires:  ocaml-oclock-devel
BuildRequires:  ocaml-uuidm-devel
BuildRequires:  ocaml-qmp-devel
BuildRequires:  ocaml-sexplib-devel
BuildRequires:  ocaml-xen-lowlevel-libs-devel
BuildRequires:  ocaml-xenstore-clients-devel
BuildRequires:  ocaml-xenstore-devel
BuildRequires:  ocaml-xcp-inventory-devel
BuildRequires:  xen-devel
BuildRequires:  ocaml-uutf-devel
BuildRequires:  ocaml-xcp-rrd-devel
BuildRequires:  ocaml-oclock-devel
BuildRequires:  ocaml-backtrace-devel
Requires:       message-switch
Requires:       redhat-lsb-core
Requires:       xenops-cli
Requires:       vncterm
Requires:       linux-guest-loader
Requires:       ocaml-xen-lowlevel-libs-runtime

%description
Simple VM manager for the xapi toolstack.

%package        xc
Summary:        Xenopsd using xc
Requires:       %{name} = %{version}-%{release}
Requires:       forkexecd
Requires:       vncterm
Requires:       xen-libs

%description    xc
Simple VM manager for Xen using libxc.

%package        simulator
Summary:        Xenopsd simulator
Requires:       %{name} = %{version}-%{release}

%description    simulator
A synthetic VM manager for testing.

%package        xenlight
Summary:        Xenopsd using libxenlight
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}
%description    xenlight
Simple VM manager for Xen using libxenlight

%prep
%setup -q
cp %{SOURCE1} xenopsd-xc-init
cp %{SOURCE2} xenopsd-simulator-init
cp %{SOURCE4} xenopsd-xenlight-init
cp %{SOURCE5} make-xsc-xenopsd.conf
cp %{SOURCE6} xenopsd-network-conf
cp %{SOURCE7} xenopsd-vncterm-wrapper

%build
./configure --libexecdir %{_libexecdir}/%{name}
make

%install
mkdir -p %{buildroot}/%{_sbindir}

install -D _build/simulator/xenops_simulator_main.native %{buildroot}/%{_sbindir}/xenopsd-simulator
install -D _build/xc/xenops_xc_main.native               %{buildroot}/%{_sbindir}/xenopsd-xc
install -D _build/xl/xenops_xl_main.native               %{buildroot}/%{_sbindir}/xenopsd-xenlight
install -D -m 0755 xenopsd-xenlight-init %{buildroot}/%{_sysconfdir}/init.d/xenopsd-xenlight
mkdir -p %{buildroot}/%{_libexecdir}/%{name}
install -D scripts/vif %{buildroot}/%{_libexecdir}/%{name}/vif
install -D scripts/vif-real %{buildroot}/%{_libexecdir}/%{name}/vif-real
install -D scripts/block %{buildroot}/%{_libexecdir}/%{name}/block
install -D scripts/qemu-dm-wrapper %{buildroot}/%{_libexecdir}/%{name}/qemu-dm-wrapper
install -D xenopsd-vncterm-wrapper %{buildroot}/%{_libexecdir}/%{name}/vncterm-wrapper
install -D scripts/qemu-vif-script %{buildroot}/%{_libexecdir}/%{name}/qemu-vif-script
install -D scripts/setup-vif-rules %{buildroot}/%{_libexecdir}/%{name}/setup-vif-rules
install -D scripts/common.py %{buildroot}/%{_libexecdir}/%{name}/common.py
install -D scripts/network.conf %{buildroot}/%{_libexecdir}/%{name}/network.conf

mkdir -p %{buildroot}%{_sysconfdir}/init.d
install -m 0755 xenopsd-xc-init %{buildroot}/%{_sysconfdir}/init.d/xenopsd-xc
install -m 0755 xenopsd-simulator-init %{buildroot}/%{_sysconfdir}/init.d/xenopsd-simulator

mkdir -p %{buildroot}/etc/xapi
chmod 755 make-xsc-xenopsd.conf 
LIBEXECDIR=%{_libexecdir}/%{name} ETCDIR=/etc/xapi SCRIPTSDIR=%{_libexecdir}/%{name} DESTDIR=%{buildroot} ./make-xsc-xenopsd.conf > xenopsd-conf
install -m 0644 xenopsd-conf %{buildroot}/etc/xenopsd.conf
install -m 0644 xenopsd-network-conf %{buildroot}/etc/xapi/network.conf


%files
%doc README.md LICENSE
%{_libexecdir}/%{name}/vif
%{_libexecdir}/%{name}/vif-real
%{_libexecdir}/%{name}/block
%{_libexecdir}/%{name}/qemu-dm-wrapper
%{_libexecdir}/%{name}/vncterm-wrapper
%{_libexecdir}/%{name}/qemu-vif-script
%{_libexecdir}/%{name}/setup-vif-rules
%{_libexecdir}/%{name}/network.conf
%{_libexecdir}/%{name}/common.py
%{_libexecdir}/%{name}/common.pyo
%{_libexecdir}/%{name}/common.pyc
/etc/xenopsd.conf
/etc/xapi/network.conf

%files xc
%{_sbindir}/xenopsd-xc
%{_sysconfdir}/init.d/xenopsd-xc

%post xc
/sbin/chkconfig --add xenopsd-xc

%preun xc
if [ $1 -eq 0 ]; then
  /sbin/service xenopsd-xc stop > /dev/null 2>&1
  /sbin/chkconfig --del xenopsd-xc
fi

%files simulator
%{_sbindir}/xenopsd-simulator
%{_sysconfdir}/init.d/xenopsd-simulator

%post simulator
/sbin/chkconfig --add xenopsd-simulator

%preun simulator
if [ $1 -eq 0 ]; then
  /sbin/service xenopsd-simulator stop > /dev/null 2>&1
  /sbin/chkconfig --del xenopsd-simulator
fi

%files xenlight
%defattr(-,root,root)
%{_sbindir}/xenopsd-xenlight
%{_sysconfdir}/init.d/xenopsd-xenlight

%post xenlight
/sbin/chkconfig --add xenopsd-xenlight

%preun xenlight
if [ $1 -eq 0 ]; then
  /sbin/service xenopsd-xenlight stop > /dev/null 2>&1
  /sbin/chkconfig --del xenopsd-xenlight
fi

%changelog
* Wed Sep 9 2015 David Scott <dave.scott@citrix.com> - 0.12.0-1
- Update to 0.12.0

* Fri Aug 14 2015 David Scott <dave.scott@citrix.com> - 0.11.0-1
- Update to 0.11.0

* Tue Apr  7 2015 David Scott <dave.scott@citrix.com> - 0.10.1-1
- Update to 0.10.1

* Fri Apr  3 2015 David Scott <dave.scott@citrix.com> - 0.9.46-4
- Update to cohttp.0.15.2

* Thu Feb  5 2015 David Scott <dave.scott@citrix.com> - 0.9.46-3
- Backport libxl blkback fix

* Wed Jan 28 2015 David Scott <dave.scott@citrix.com> - 0.9.46-2
- Attempt to backport libxl workaround

* Wed Jan 21 2015 David Scott <dave.scott@citrix.com> - 0.9.46-1
- Update to 0.9.46

* Sun Oct 19 2014 David Scott <dave.scott@citrix.com> - 0.9.45-2
- Add patch to fix the upstream qemu 4MiB videoram issue
- Add patch to fix the device id upgrade issue

* Tue Oct 14 2014 David Scott <dave.scott@citrix.com> - 0.9.45-1
- Update to 0.9.45

* Mon Sep 22 2014 David Scott <dave.scott@citrix.com> - 0.9.44-1
- Update to 0.9.44

* Mon Sep 8 2014 David Scott <dave.scott@citrix.com> - 0.9.43-4
- Add a search-path to the xenopsd.conf

* Thu Sep 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.43-3
- Remove xen-missing-headers dependency

* Thu Sep 4 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.43-2
- Reinstate xenlight package in CentOS

* Sun Aug 24 2014 David Scott <dave.scott@citrix.com> - 0.9.43-1
- Update to 0.9.43 which supports OCaml 4.01.0

* Fri Aug 22 2014 David Scott <dave.scott@citrix.com> - 0.9.41-1
- Update to 0.9.41: now pygrub, eliloader, hvmloader and vncterm
  are optional

* Fri Aug 22 2014 David Scott <dave.scott@citrix.com> - 0.9.39-5
- vncterm-wrapper: ensure the groups are added on startup.

* Fri Aug 22 2014 David Scott <dave.scott@citrix.com> - 0.9.39-4
- Add a vncterm-wrapper: needed to locate the qemu keymaps

* Thu Aug 21 2014 David Scott <dave.scott@citrix.com> - 0.9.39-2
- Include {vbd,vif}-xl in the package

* Wed Aug 20 2014 David Scott <dave.scott@citrix.com> - 0.9.39-2
- Package xenopsd-xenlight

* Wed Aug 20 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 0.9.39-1
- Update to 0.9.39 which compiles without warnings

* Tue Aug 19 2014 David Scott <dave.scott@citrix.com> - 0.9.38-1
- Update to 0.9.38 with better libxl support

* Sat Jun 21 2014 David Scott <dave.scott@citrix.com> - 0.9.37-1
- Depend on the ocaml-xen-lowlevel-libs-runtime package
- Don't include xenguest: this now comes from ocaml-xen-lowlevel-libs

* Fri Jun  6 2014 Jonathan Ludlam <jonathan.ludlam@citrix.com> - 0.9.37-1
- Update to 0.9.37

* Fri Jan 17 2014 Euan Harris <euan.harris@eu.citrix.com> - 0.9.34-1
- Update to 0.9.34, restoring fixes from the 0.9.32 line which were 
  not merged to trunk before 0.9.33 was tagged

* Wed Dec 4 2013 Euan Harris <euan.harris@eu.citrix.com> - 0.9.33-1
- Update to 0.9.33, with fixes for suspending and resuming HVM guests

* Mon Oct 28 2013 David Scott <dave.scott@eu.citrix.com> - 0.9.32-1
- Update to 0.9.32, with udev fix (no more "task was asynchronously cancelled")

* Mon Oct 21 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.31
- move scripts back to libexecdir

* Sun Oct 20 2013 David Scott <dave.scott@eu.citrix.com>
- give up on making libxl work, since it requires xen-4.4
- move scripts from libexecdir to libdir

* Fri Oct 18 2013 David Scott <dave.scott@eu.citrix.com>
- update to 0.9.29

* Fri Oct 18 2013 David Scott <dave.scott@eu.citrix.com>
- update to 0.9.28

* Wed Sep 25 2013 David Scott <dave.scott@eu.citrix.com>
- modprobe blk{tap,back} in the xenopsd-xc init.d script since
  we need these to make virtual disks work
- update to 0.9.27

* Tue Sep 24 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.26, which includes fixes for networking and libxl

* Fri Sep 20 2013 Euan Harris <euan.harris@citrix.com>
- Generate xenopsd.conf automatically

* Mon Sep 16 2013 Euan Harris <euan.harris@citrix.com>
- Update to 0.9.25, which includes linker paths required on Debian

* Tue Sep 10 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.24

* Fri Jun 21 2013 David Scott <dave.scott@eu.citrix.com>
- Update to 0.9.5, which includes xenopsd-xenlight

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com>
- Initial package
