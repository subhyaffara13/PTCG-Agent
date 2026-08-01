
def _verify_peercerts_impl(
    ssl_context: ssl.SSLContext,
    cert_chain: list[bytes],
    server_hostname: str | None = None,
) -> None:
    certs = None
    policies = None
    trust = None
    try:
        # Only set a hostname on the policy if we're verifying the hostname
        # on the leaf certificate.
        if server_hostname is not None and ssl_context.check_hostname:
            cf_str_hostname = None
            try:
                cf_str_hostname = _bytes_to_cf_string(server_hostname.encode("ascii"))
                ssl_policy = Security.SecPolicyCreateSSL(True, cf_str_hostname)
            finally:
                if cf_str_hostname:
                    CoreFoundation.CFRelease(cf_str_hostname)
        else:
            ssl_policy = Security.SecPolicyCreateSSL(True, None)

        policies = ssl_policy
        if ssl_context.verify_flags & ssl.VERIFY_CRL_CHECK_CHAIN:
            # Add explicit policy requiring positive revocation checks
            policies = CoreFoundation.CFArrayCreateMutable(
                CoreFoundation.kCFAllocatorDefault,
                0,
                ctypes.byref(CoreFoundation.kCFTypeArrayCallBacks),
            )
            CoreFoundation.CFArrayAppendValue(policies, ssl_policy)
            CoreFoundation.CFRelease(ssl_policy)
            revocation_policy = Security.SecPolicyCreateRevocation(
                kSecRevocationUseAnyAvailableMethod
                | kSecRevocationRequirePositiveResponse
            )
            CoreFoundation.CFArrayAppendValue(policies, revocation_policy)
            CoreFoundation.CFRelease(revocation_policy)
        elif ssl_context.verify_flags & ssl.VERIFY_CRL_CHECK_LEAF:
            raise NotImplementedError("VERIFY_CRL_CHECK_LEAF not implemented for macOS")

        certs = None
        try:
            certs = _der_certs_to_cf_cert_array(cert_chain)

            # Now that we have certificates loaded and a SecPolicy
            # we can finally create a SecTrust object!
            trust = Security.SecTrustRef()
            Security.SecTrustCreateWithCertificates(
                certs, policies, ctypes.byref(trust)
            )

        finally:
            # The certs are now being held by SecTrust so we can
            # release our handles for the array.
            if certs:
                CoreFoundation.CFRelease(certs)

        # If there are additional trust anchors to load we need to transform
        # the list of DER-encoded certificates into a CFArray.
        ctx_ca_certs_der: list[bytes] | None = ssl_context.get_ca_certs(
            binary_form=True
        )
        if ctx_ca_certs_der:
            ctx_ca_certs = None
            try:
                ctx_ca_certs = _der_certs_to_cf_cert_array(ctx_ca_certs_der)
                Security.SecTrustSetAnchorCertificates(trust, ctx_ca_certs)
            finally:
                if ctx_ca_certs:
                    CoreFoundation.CFRelease(ctx_ca_certs)

        # We always want system certificates.
        Security.SecTrustSetAnchorCertificatesOnly(trust, False)

        # macOS 10.13 and earlier don't support SecTrustEvaluateWithError()
        # so we use SecTrustEvaluate() which means we need to construct error
        # messages ourselves.
        if _is_macos_version_10_14_or_later:
            _verify_peercerts_impl_macos_10_14(ssl_context, trust)
        else:
            _verify_peercerts_impl_macos_10_13(ssl_context, trust)
    finally:
        if policies:
            CoreFoundation.CFRelease(policies)
        if trust:
            CoreFoundation.CFRelease(trust)


def _verify_peercerts_impl(
    ssl_context: ssl.SSLContext,
    cert_chain: list[bytes],
    server_hostname: str | None = None,
) -> None:
    # This is a no-op because we've enabled SSLContext's built-in
    # verification via verify_mode=CERT_REQUIRED, and don't need to repeat it.
    pass


def _verify_peercerts_impl(
    ssl_context: ssl.SSLContext,
    cert_chain: list[bytes],
    server_hostname: str | None = None,
) -> None:
    """Verify the cert_chain from the server using Windows APIs."""

    # If the peer didn't send any certificates then
    # we can't do verification. Raise an error.
    if not cert_chain:
        raise ssl.SSLCertVerificationError("Peer sent no certificates to verify")

    pCertContext = None
    hIntermediateCertStore = CertOpenStore(CERT_STORE_PROV_MEMORY, 0, None, 0, None)
    try:
        # Add intermediate certs to an in-memory cert store
        for cert_bytes in cert_chain[1:]:
            CertAddEncodedCertificateToStore(
                hIntermediateCertStore,
                X509_ASN_ENCODING | PKCS_7_ASN_ENCODING,
                cert_bytes,
                len(cert_bytes),
                CERT_STORE_ADD_USE_EXISTING,
                None,
            )

        # Cert context for leaf cert
        leaf_cert = cert_chain[0]
        pCertContext = CertCreateCertificateContext(
            X509_ASN_ENCODING | PKCS_7_ASN_ENCODING, leaf_cert, len(leaf_cert)
        )

        # Chain params to match certs for serverAuth extended usage
        cert_enhkey_usage = CERT_ENHKEY_USAGE()
        cert_enhkey_usage.cUsageIdentifier = 1
        cert_enhkey_usage.rgpszUsageIdentifier = (c_char_p * 1)(OID_PKIX_KP_SERVER_AUTH)
        cert_usage_match = CERT_USAGE_MATCH()
        cert_usage_match.Usage = cert_enhkey_usage
        chain_params = CERT_CHAIN_PARA()
        chain_params.RequestedUsage = cert_usage_match
        chain_params.cbSize = sizeof(chain_params)
        pChainPara = pointer(chain_params)

        if ssl_context.verify_flags & ssl.VERIFY_CRL_CHECK_CHAIN:
            chain_flags = CERT_CHAIN_REVOCATION_CHECK_CHAIN
        elif ssl_context.verify_flags & ssl.VERIFY_CRL_CHECK_LEAF:
            chain_flags = CERT_CHAIN_REVOCATION_CHECK_END_CERT
        else:
            chain_flags = 0

        try:
            # First attempt to verify using the default Windows system trust roots
            # (default chain engine).
            _get_and_verify_cert_chain(
                ssl_context,
                None,
                hIntermediateCertStore,
                pCertContext,
                pChainPara,
                server_hostname,
                chain_flags=chain_flags,
            )
        except ssl.SSLCertVerificationError as e:
            # If that fails but custom CA certs have been added
            # to the SSLContext using load_verify_locations,
            # try verifying using a custom chain engine
            # that trusts the custom CA certs.
            custom_ca_certs: list[bytes] | None = ssl_context.get_ca_certs(
                binary_form=True
            )
            if custom_ca_certs:
                try:
                    _verify_using_custom_ca_certs(
                        ssl_context,
                        custom_ca_certs,
                        hIntermediateCertStore,
                        pCertContext,
                        pChainPara,
                        server_hostname,
                        chain_flags=chain_flags,
                    )
                # Raise the original error, not the new error.
                except ssl.SSLCertVerificationError:
                    raise e from None
            else:
                raise
    finally:
        CertCloseStore(hIntermediateCertStore, 0)
        if pCertContext:
            CertFreeCertificateContext(pCertContext)

