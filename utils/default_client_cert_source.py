
def default_client_cert_source():
    """Get a callback which returns the default client SSL credentials.

    Returns:
        Callable[[], [bytes, bytes]]: A callback which returns the default
            client certificate bytes and private key bytes, both in PEM format.

    Raises:
        google.auth.exceptions.DefaultClientCertSourceError: If the default
            client SSL credentials don't exist or are malformed.
    """
    if not has_default_client_cert_source(include_context_aware=True):
        raise exceptions.MutualTLSChannelError(
            "Default client cert source doesn't exist"
        )

    def callback():
        try:
            _, cert_bytes, key_bytes = _mtls_helper.get_client_cert_and_key()
        except (OSError, RuntimeError, ValueError) as caught_exc:
            new_exc = exceptions.MutualTLSChannelError(caught_exc)
            raise new_exc from caught_exc

        return cert_bytes, key_bytes

    return callback


def default_client_cert_source():
    """Get a callback which returns the default client SSL credentials.

    Returns:
        Awaitable[Callable[[], Tuple[bytes, bytes]]]: A callback which returns the default
            client certificate bytes and private key bytes, both in PEM format.

    Raises:
        google.auth.exceptions.DefaultClientCertSourceError: If the default
            client SSL credentials don't exist or are malformed.
    """
    if not google.auth.transport.mtls.has_default_client_cert_source(
        include_context_aware=False
    ):
        raise exceptions.MutualTLSChannelError(
            "Default client cert source doesn't exist"
        )

    async def callback():
        try:
            _, cert_bytes, key_bytes = await get_client_cert_and_key()
        except (OSError, RuntimeError, ValueError) as caught_exc:
            new_exc = exceptions.MutualTLSChannelError(caught_exc)
            raise new_exc from caught_exc

        return cert_bytes, key_bytes

    return callback

