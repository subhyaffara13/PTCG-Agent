from typing import Optional

def make_client_cert_ssl_context(
    cert_bytes: bytes, key_bytes: bytes, passphrase: Optional[bytes] = None
) -> ssl.SSLContext:
    """Creates an SSLContext with the given client certificate and key.
    This function writes the certificate and key to temporary files so that
    ssl.create_default_context can load them, as the ssl module requires
    file paths for client certificates. These temporary files are deleted
    immediately after the SSL context is created.
    Args:
        cert_bytes (bytes): The client certificate content in PEM format.
        key_bytes (bytes): The client private key content in PEM format.
        passphrase (Optional[bytes]): The passphrase for the private key, if any.
    Returns:
        ssl.SSLContext: The configured SSL context with client certificate.

    Raises:
        google.auth.exceptions.TransportError: If there is an error loading the certificate.
    """
    with _create_temp_file(cert_bytes) as cert_path, _create_temp_file(
        key_bytes
    ) as key_path:
        try:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_cert_chain(
                certfile=cert_path, keyfile=key_path, password=passphrase
            )
            return context
        except (ssl.SSLError, OSError, IOError, ValueError, RuntimeError) as exc:
            raise exceptions.TransportError(
                "Failed to load client certificate and key for mTLS."
            ) from exc

