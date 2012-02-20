# This spec is based on Toni Graffy's from OpenSUSE and
# Alberto Altieri's from MIB work

Name:		cobra
Version:	0.98.4
Release:	%mkrel 1
Summary:	Java HTML Renderer & Parser
URL:		http://lobobrowser.org/cobra.jsp
Source0:	http://sourceforge.net/projects/xamj/files/Cobra%20HTML%20Toolkit/%{version}/%{name}-%{version}.zip
Group:		Development/Java
License:	LGPL
BuildRequires:	dos2unix
BuildRequires:	java-devel-openjdk
BuildRequires:	rhino
BuildRequires:	unzip
BuildRequires:	update-alternatives
BuildRequires:	xerces-j2
BuildRequires:	xmlbeans
BuildRequires:	xml-commons-apis
Requires:	java >= 1.6
Requires:	rhino
BuildArch:	noarch

%description
Cobra is a pure Java HTML renderer and DOM parser that is being
developed to support HTML 4, Javascript and CSS 2.

Cobra can be used as a Javascript-aware and CSS-aware HTML parser,
independently of the Cobra rendering engine. Javascript DOM modifications
that occur during parsing (e.g. via document.write) will be reflected
in the parsed DOM, unless Javascript is disabled.

%package javadoc
Summary:	Javadoc for cobra
Group:		Documentation/HTML
PreReq:		coreutils

%description javadoc
Javadoc for package cobra.

%prep
%setup -q

dos2unix     *.txt doc/api/stylesheet.css
%__chmod 644 *.txt doc/api/stylesheet.css

# remove the files we want to build
%__rm -r lib

%build
%__install -dm 755 classes
javac \
	-encoding iso-8859-1 \
	-d classes \
	-cp `build-classpath js` \
	`find . -name '*.java'`

jar \
	cf %{name}.jar \
	-C classes . \

%install
%__rm -rf %{buildroot}
export NO_BRP_CHECK_BYTECODE_VERSION=true

# jars
%__install -dm 755 %{buildroot}%{_javadir}/%{name}
%__install -pm 644 %{name}.jar \
	%{buildroot}%{_javadir}/%{name}/%{name}-%{version}.jar
pushd %{buildroot}%{_javadir}/%{name}
	for jar in *-%{version}*; do \
		ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; \
	done

	# link rhino to allow `build-classpath cobra`
	%__ln_s %{_javadir}/js.jar .
popd

# javadoc
%__install -dm 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
%__cp -pr doc/* \
	%{buildroot}%{_javadocdir}/%{name}-%{version}
%__ln_s %{name}-%{version} \
	%{buildroot}%{_javadocdir}/%{name} # ghost symlink

%clean
%__rm -rf %{buildroot}

%post javadoc
%__rm -f %{_javadocdir}/%{name}
%__ln_s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(-,root,root)
%doc *.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/*.jar

%files javadoc
%defattr(-,root,root)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

