Summary:	An easy-to-use self-sufficient web server
Name:		mongoose
Version:	3.1
Release:	5
License:	MIT
Group:		Applications/System
Source0:	http://mongoose.googlecode.com/files/%{name}-%{version}.tgz
# Source0-md5:	e718fc287b4eb1bd523be3fa00942bb0
Source1:	%{name}.conf
URL:		http://code.google.com/p/mongoose
BuildRequires:	openssl-devel
# Build changes:
# http://code.google.com/p/mongoose/issues/detail?id=372
Patch0:		%{name}-fix-libmongoose-so-build.patch
# http://code.google.com/p/mongoose/issues/detail?id=371
Patch1:		%{name}-fix-no-ssl-dl-build-error.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mongoose web server executable is self-sufficient, it does not depend
on anything to start serving requests. If it is copied to any
directory and executed, it starts to serve that directory on port 8080
(so to access files, go to http://localhost:8080). If some additional
configuration is required - for example, different listening port or
IP-based access control, then a 'mongoose.conf' file with respective
options can be created in the same directory where executable lives.
This makes Mongoose perfect for all sorts of demos, quick tests, file
sharing, and Web programming.

%package libs
Summary:	Shared Object for applications that use %{name} embedded
Group:		Development/Libraries

%description libs
This package contains the shared library required by applications that
are using %{name}'s embeddable API to provide web services.

%package devel
Summary:	Header files and development libraries for %{name}
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files and development libraries for
%{name}. If you like to develop programs embedding %{name} on them,
you will need to install %{name}-devel and check %{name}'s API at its
comprisable header file.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .solib-build
%patch1 -p1 -b .nossldl-build
install -p -m 0644  %{SOURCE1} .

%build
export VERSION=%{version}
%{__make} \
	CC="%{__cc}" \
	VER="$VERSION" \
	SOVER="${VERSION%.?}" \
	CFLAGS="%{rpmcflags} -lssl -lcrypto -DNO_SSL_DL" \
	linux

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir},%{_includedir}}
install -p %{name} $RPM_BUILD_ROOT%{_bindir}
cp -p %{name}.1 $RPM_BUILD_ROOT%{_mandir}/man1

# -lib subpackage
VERSION=%{version}
install -p lib%{name}.so.%{version} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.$VERSION
ln -s lib%{name}.so.$VERSION $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so.${VERSION%.?}

# -devel subpackage
cp -p %{name}.h $RPM_BUILD_ROOT%{_includedir}
ln -s lib%{name}.so.$VERSION $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{name}.conf LICENSE
%attr(755,root,root) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib%{name}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/lib%{name}.so.3

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}.so
