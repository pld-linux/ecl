%define	_patchlevel	p1
Summary:	Embeddable Common Lisp
Summary(pl.UTF-8):	Osadzalny Common Lisp
Name:		ecl
Version:	0.9j
Release:	1.%{_patchlevel}.1
License:	GPL v2
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/sourceforge/ecls/%{name}-%{version}-%{_patchlevel}.tgz
# Source0-md5:	2e20a0fcad15f323b233488bbaef636a
URL:		http://ecls.sourceforge.net/
BuildRequires:	gc-devel
BuildRequires:	gmp-devel
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ECL is a Common Lisp implementation initially developed by Giuseppe
Attardi and currently maintained by Juan Jose Garcia-Ripoll. ECL is
the successor to EcoLisp.  It works by compiling Lisp code to C and
invoking C compiler.

%description -l pl.UTF-8
ECL jest implementacją języka Common Lisp pierwotnie opracowaną przez
Giuseppe Attardiego, obecnie zaś utrzymywaną przez Juana Jose
Garcia-Ripoll.  ECL jest następcą implementacji EcoLisp.  Działa
kompilując kod Lispa do C i wywołując kompilator C.

%prep
%setup -q

# remove CVS control files
find -name CVS -print0 | xargs -0 rm -rf

%build

# Make ./configure wrapper accept spaces in arguments
%{__sed} -i 's/\$\*/"${@}"/' ./configure

%configure \
    --enable-boehm=system \
    --with-system-gmp \
    --with-__thread

# Fix a typo
%{__sed} -i 's!..ANNOUNCEMENT!../ANNOUNCEMENT!' build/doc/Makefile

%{__make} all doc

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C ./build/doc install \
	DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_examplesdir}
cp -R examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ANNOUNCEMENT Copyright build/doc/*.html
%{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/libecl.so
%{_includedir}/%{name}
%attr(755,root,root) %{_bindir}/*
%{_examplesdir}/%{name}-%{version}
%{_infodir}/%{name}*
%{_mandir}/*/*
