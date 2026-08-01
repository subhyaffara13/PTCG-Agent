
def inject_into_ssl() -> None:
    """Injects the :class:`truststore.SSLContext` into the ``ssl``
    module by replacing :class:`ssl.SSLContext`.
    """
    setattr(ssl, "SSLContext", SSLContext)
    # urllib3 holds on to its own reference of ssl.SSLContext
    # so we need to replace that reference too.
    try:
        import pip._vendor.urllib3.util.ssl_ as urllib3_ssl

        setattr(urllib3_ssl, "SSLContext", SSLContext)
    except ImportError:
        pass

    # requests starting with 2.32.0 added a preloaded SSL context to improve concurrent performance;
    # this unfortunately leads to a RecursionError, which can be avoided by patching the preloaded SSL context with
    # the truststore patched instance
    # also see https://github.com/psf/requests/pull/6667
    try:
        from pip._vendor.requests import adapters as requests_adapters

        preloaded_context = getattr(requests_adapters, "_preloaded_ssl_context", None)
        if preloaded_context is not None:
            setattr(
                requests_adapters,
                "_preloaded_ssl_context",
                SSLContext(ssl.PROTOCOL_TLS_CLIENT),
            )
    except ImportError:
        pass

