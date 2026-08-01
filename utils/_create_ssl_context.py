
def _create_ssl_context(
    cafile: Optional[str],
    ssl_security_level: Optional[str],
    ssl_ecdh_curve: Optional[str],
) -> ssl.SSLContext:
    """
    Create an SSL context with the given configuration.
    This is separated from get_ssl_configuration to enable caching.
    """
    custom_ssl_context = ssl.create_default_context(cafile=cafile)

    # Optimize SSL handshake performance
    # Set minimum TLS version to 1.2 for better performance
    custom_ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2

    # Configure cipher suites for optimal performance
    if ssl_security_level and isinstance(ssl_security_level, str):
        # User provided custom cipher configuration (e.g., via SSL_SECURITY_LEVEL env var)
        custom_ssl_context.set_ciphers(ssl_security_level)
    else:
        # Use optimized cipher list that strongly prefers fast ciphers
        # but falls back to widely compatible ones
        custom_ssl_context.set_ciphers(DEFAULT_SSL_CIPHERS)

    # Configure ECDH curve for key exchange (e.g., to disable PQC and improve performance)
    # Set SSL_ECDH_CURVE env var or litellm.ssl_ecdh_curve to 'X25519' to disable PQC
    # Common valid curves: X25519, prime256v1, secp384r1, secp521r1
    if ssl_ecdh_curve and isinstance(ssl_ecdh_curve, str):
        try:
            custom_ssl_context.set_ecdh_curve(ssl_ecdh_curve)
            verbose_logger.debug(f"SSL ECDH curve set to: {ssl_ecdh_curve}")
        except AttributeError:
            verbose_logger.warning(
                f"SSL ECDH curve configuration not supported. "
                f"Python version: {sys.version.split()[0]}, OpenSSL version: {ssl.OPENSSL_VERSION}. "
                f"Requested curve: {ssl_ecdh_curve}. Continuing with default curves."
            )
        except ValueError as e:
            # Invalid curve name
            verbose_logger.warning(
                f"Invalid SSL ECDH curve name: '{ssl_ecdh_curve}'. {e}. "
                f"Common valid curves: X25519, prime256v1, secp384r1, secp521r1. "
                f"Continuing with default curves (including PQC)."
            )

    return custom_ssl_context

