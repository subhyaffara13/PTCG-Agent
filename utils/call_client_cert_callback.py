
def call_client_cert_callback():
    """Calls the client cert callback and returns the certificate and key."""
    _, cert_bytes, key_bytes, passphrase = get_client_ssl_credentials(
        generate_encrypted_key=True
    )
    return cert_bytes, key_bytes

