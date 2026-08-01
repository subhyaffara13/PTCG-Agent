
def _is_agent_identity_certificate(cert):
    """Checks if a certificate is an Agent Identity certificate.

    This is determined by checking the Subject Alternative Name (SAN) for a
    SPIFFE ID with a trust domain matching Agent Identity patterns.

    Args:
        cert (cryptography.x509.Certificate): The parsed certificate object.

    Returns:
        bool: True if the certificate is an Agent Identity certificate,
            False otherwise.
    """
    try:
        from cryptography import x509
        from cryptography.x509.oid import ExtensionOID

        try:
            ext = cert.extensions.get_extension_for_oid(
                ExtensionOID.SUBJECT_ALTERNATIVE_NAME
            )
        except x509.ExtensionNotFound:
            return False
        uris = ext.value.get_values_for_type(x509.UniformResourceIdentifier)

        for uri in uris:
            parsed_uri = urlparse(uri)
            if parsed_uri.scheme == "spiffe":
                trust_domain = parsed_uri.netloc
                for pattern in _AGENT_IDENTITY_SPIFFE_TRUST_DOMAIN_PATTERNS:
                    if re.match(pattern, trust_domain):
                        return True
        return False
    except ImportError as e:
        raise ImportError(CRYPTOGRAPHY_NOT_FOUND_ERROR) from e

