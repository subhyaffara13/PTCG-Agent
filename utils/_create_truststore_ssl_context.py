
def _create_truststore_ssl_context() -> SSLContext | None:
    try:
        import ssl
    except ImportError:
        logger.warning("Disabling truststore since ssl support is missing")
        return None

    try:
        from pip._vendor import truststore
    except ImportError:
        logger.warning("Disabling truststore because platform isn't supported")
        return None

    ctx = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.load_verify_locations(certifi.where())
    return ctx

