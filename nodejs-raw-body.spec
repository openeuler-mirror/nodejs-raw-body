%{?nodejs_find_provides_and_requires}

%global enable_tests 1

Name:                nodejs-raw-body
Version:             2.2.0
Release:             1
Summary:             Get and validate the raw body of a readable stream
License:             MIT
URL:                 https://github.com/stream-utils/raw-body
Source0:             http://registry.npmjs.org/raw-body/-/raw-body-%{version}.tgz
#git clone git://github.com/stream-utils/raw-body.git
#cd raw-body
#git archive --prefix="test/" --format=tar tags/${tag}:test/ \
#    | bzip2 > "$pwd"/tests-${tag}.tar.bz2
Source1:             tests-%{version}.tar.bz2

ExclusiveArch:       %{nodejs_arches} noarch
BuildArch:           noarch
BuildRequires:       nodejs-packaging
BuildRequires:       npm(bytes) npm(iconv-lite) npm(unpipe)

%if 0%{?enable_tests}
BuildRequires:       npm(bluebird) npm(istanbul)
Buildrequires:       npm(mocha)
BuildRequires:       npm(readable-stream) npm(through2)
%endif

%description
This module gets the entire buffer of a stream either as a buffer or a string.
It validates the stream's length against an expected length and maximum limit.
It is ideal for parsing request bodies.

%prep
%setup -q -n package
%setup -q -T -D -a 1 -n package
%nodejs_fixdep bytes --caret
%nodejs_fixdep iconv-lite '<0.5.0'
%nodejs_fixdep unpipe --caret

%build
#nothing to do

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/raw-body
cp -pr package.json index.js \
    %{buildroot}%{nodejs_sitelib}/raw-body

%nodejs_symlink_deps

%check
%nodejs_symlink_deps --check
%{__nodejs} -e 'require("./")'

%if 0%{?enable_tests}
mocha --trace-deprecation --reporter spec --bail --check-leaks test/
istanbul-js cover mocha -- --trace-deprecation --reporter dot --check-leaks test/
istanbul-js cover mocha --report lcovonly -- --trace-deprecation --reporter spec --check-leaks test/
%endif

%files
%doc README.md
%license LICENSE
%{nodejs_sitelib}/raw-body

%changelog
* Wed Aug 19 2020 wangxiao <wangxiao65@huawei.com> - 2.2.0-1
- package init
