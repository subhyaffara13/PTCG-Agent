
def calculate_certificate_fingerprint(cert):
    """Calculates the URL-encoded, unpadded, base64-encoded SHA256 hash of a
    DER-encoded certificate.

    Args:
        cert (cryptography.x509.Certificate): The parsed certificate object.

    Returns:
        str: The URL-encoded, unpadded, base64-encoded SHA256 fingerprint.
    """
    try:
        from cryptography.hazmat.primitives import serialization

        der_cert = cert.public_bytes(serialization.Encoding.DER)
        fingerprint = hashlib.sha256(der_cert).digest()
        # The certificate fingerprint is generated in two steps to align with GFE's
        # expectations and ensure proper URL transmission:
        # 1. Standard base64 encoding is applied, and padding ('=') is removed.
        # 2. The resulting string is then URL-encoded to handle special characters
        #    ('+', '/') that would otherwise be misinterpreted in URL parameters.
        base64_fingerprint = base64.b64encode(fingerprint).decode("utf-8")
        unpadded_base64_fingerprint = base64_fingerprint.rstrip("=")
        return quote(unpadded_base64_fingerprint)
    except ImportError as e:
        raise ImportError(CRYPTOGRAPHY_NOT_FOUND_ERROR) from e

