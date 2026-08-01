
def parse_certificate(cert_bytes):
    """Parses a PEM-encoded certificate.

    Args:
        cert_bytes (bytes): The PEM-encoded certificate bytes.

    Returns:
        cryptography.x509.Certificate: The parsed certificate object.
    """
    try:
        from cryptography import x509

        return x509.load_pem_x509_certificate(cert_bytes)
    except ImportError as e:
        raise ImportError(CRYPTOGRAPHY_NOT_FOUND_ERROR) from e

