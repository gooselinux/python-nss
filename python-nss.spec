# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-nss
Version:        0.8
Release:        3%{?dist}
Summary:        Python bindings for Network Security Services (NSS)

Group:          Development/Languages
License:        MPLv1.1 or GPLv2+ or LGPLv2+
URL:            http://mxr.mozilla.org/security/source/security/python/nss
Source0:        %{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global docdir %{_docdir}/%{name}-%{version}

BuildRequires: python-devel
BuildRequires: python-setuptools-devel
BuildRequires: epydoc
BuildRequires: python-docutils
BuildRequires: nspr-devel
BuildRequires: nss-devel


%description
This package provides Python bindings for Network Security Services
(NSS) and the Netscape Portable Runtime (NSPR).

NSS is a set of libraries supporting security-enabled client and
server applications. Applications built with NSS can support SSL v2
and v3, TLS, PKCS #5, PKCS #7, PKCS #11, PKCS #12, S/MIME, X.509 v3
certificates, and other security standards. Specific NSS
implementations have been FIPS-140 certified.


%prep
%setup -q


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build
%{__python} setup.py build_doc


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install  -O1 --install-platlib %{python_sitearch} --skip-build --root $RPM_BUILD_ROOT
%{__python} setup.py install_doc --docdir %{docdir} --skip-build --root $RPM_BUILD_ROOT

# Include httplib ported to NSS as example
cp lib/httplib.py $RPM_BUILD_ROOT/%{docdir}/examples

# Include digest and cipher tests as example
cp test/digest_test.py $RPM_BUILD_ROOT/%{docdir}/examples
cp test/cipher_test.py $RPM_BUILD_ROOT/%{docdir}/examples

# Remove execution permission from any example scripts
find $RPM_BUILD_ROOT/%{docdir}/examples -type f | xargs chmod a-x

# Set correct permissions on .so files
chmod 0755 $RPM_BUILD_ROOT/%{python_sitearch}/nss/*.so


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc %{docdir}
%{python_sitearch}/*


%changelog
* Tue Apr  6 2010 John Dennis <jdennis@redhat.com> - 0.8-3
- fix URL tag in spec file per package wrangler review request
  Related: rhbz#543948

* Wed Mar 24 2010 John Dennis <jdennis@redhat.com> - 0.8-2
- change %%define to %%global per spec file review request
  Related: rhbz#543948

* Mon Sep 21 2009 John Dennis <jdennis@redhat.com> - 0.8-1
- The following methods, properties  and functions were added:
  SecItem.type SecItem.len, SecItem.data
  PK11SymKey.key_data, PK11SymKey.key_length, PK11SymKey.slot
  create_context_by_sym_key
  param_from_iv
  generate_new_param
  get_iv_length
  get_block_size
  get_pad_mechanism
- SecItem's now support indexing and slicing on their data
- Clean up parsing and parameter validation of variable arg functions

* Fri Sep 18 2009 John Dennis <jdennis@redhat.com> - 0.7-1
- add support for symmetric encryption/decryption
  more support for digests (hashes)

  The following classes were added:
  PK11SymKey PK11Context

  The following methods and functions were added:
  get_best_wrap_mechanism          get_best_key_length
  key_gen                          derive
  get_key_length                   digest_key
  clone_context                    digest_begin
  digest_op                        cipher_op
  finalize                         digest_final
  read_hex                         hash_buf
  sec_oid_tag_str                  sec_oid_tag_name
  sec_oid_tag_from_name            key_mechanism_type_name
  key_mechanism_type_from_name     pk11_attribute_type_name
  pk11_attribute_type_from_name    get_best_slot
  get_internal_key_slot            create_context_by_sym_key
  import_sym_key                   create_digest_context
  param_from_iv                    param_from_algid
  generate_new_param               algtag_to_mechanism
  mechanism_to_algtag

  The following files were added:
  cipher_test.py digest_test.py

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  9 2009 John Dennis <jdennis@redhat.com> - 0.6-2
- restore nss.nssinit(), make deprecated

* Wed Jul  8 2009 John Dennis <jdennis@redhat.com> - 0.6-1
- fix bug #510343 client_auth_data_callback seg faults if False
  is returned from callback

* Wed Jul  1 2009 John Dennis <jdennis@redhat.com> - 0.5-1
- restore ssl.nss_init and ssl.nss_shutdown but make them deprecated
  add __version__ string to nss module

* Tue Jun 30 2009 John Dennis <jdennis@redhat.com> - 0.4-1
- add binding for NSS_NoDB_Init(), bug #509002
  move nss_init and nss_shutdown from ssl module to nss module

* Thu Jun  4 2009 John Dennis <jdennis@redhat.com> - 0.3-1
- installed source code in Mozilla CVS repository
  update URL tag to point to CVS repositoy
  (not yet a valid URL, still have to coordinate with Mozilla)
  minor tweak to src directory layout

* Mon Jun  1 2009 John Dennis <jdennis@redhat.com> - 0.2-1
- Convert licensing to MPL tri-license
- apply patch from bug #472805, (Miloslav Trmač)
  Don't allow closing a socket twice, that causes crashes.
  New function nss.io.Socket.new_socket_pair()
  New function nss.io.Socket.poll()
  New function nss.io.Socket.import_tcp_socket()
  New method nss.nss.Certificate.get_subject_common_name()
  New function nss.nss.generate_random()
  Fix return value creation in SSLSocket.get_security_status
  New function nss.ssl.SSLSocket.import_tcp_socket()

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.1-2
- Rebuild for Python 2.6

* Tue Sep  9 2008 John Dennis <jdennis@redhat.com> - 0.1-1
- clean up ssl_example.py, fix arg list in get_cert_nicknames,
   make certdir cmd line arg consistent with other NSS tools
- update httplib.py to support client auth, add httplib_example.py which illustrates it's use
- fix some documentation
- fix some type usage which were unsafe on 64-bit

* Wed Jul  9 2008 John Dennis <jdennis@redhat.com> - 0.0-2
- add docutils to build requires so restructured text works

* Fri Jun 27 2008 John Dennis <jdennis@redhat.com> - 0.0-1
- initial release


