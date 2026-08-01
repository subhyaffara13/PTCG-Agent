
def get_cached_cert_fingerprint(cached_cert):
    """Returns the fingerprint of the cached certificate."""
    if cached_cert:
        cert_obj = parse_certificate(cached_cert)
        cached_cert_fingerprint = calculate_certificate_fingerprint(cert_obj)
    else:
        raise ValueError("mTLS connection is not configured.")
    return cached_cert_fingerprint

