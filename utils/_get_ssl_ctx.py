
def _get_ssl_ctx(
        certfile: str,
        keyfile: str,
        protocol: int,
        cafile: Optional[str] = None,
        capath: Optional[str] = None,
        client_auth_required: bool = False,
) -> ssl.SSLContext:
    """Load context supports SSL."""
    ssl_cxt = ssl.SSLContext(protocol=protocol)

    if cafile is not None or capath is not None:
        try:
            ssl_cxt.load_verify_locations(cafile, capath)
        except IOError as exc:
            exc_type = type(exc)
            msg = str(exc)
            raise exc_type(f"Cannot load CA certificate chain from file "
                           f"{cafile!r} or directory {capath!r}: {msg}")
    else:
        try:
            ssl_cxt.load_default_certs(purpose=ssl.Purpose.CLIENT_AUTH)
        except IOError as exc:
            exc_type = type(exc)
            msg = str(exc)
            raise exc_type(f"Cannot load default CA certificate chain: {msg}")

    if client_auth_required:
        ssl_cxt.verify_mode = ssl.CERT_REQUIRED

    try:
        ssl_cxt.load_cert_chain(certfile=certfile, keyfile=keyfile)
    except IOError as exc:
        exc_type = type(exc)
        msg = str(exc)
        raise exc_type(f"Cannot load server certificate file {certfile!r} or "
                       f"its private key file {keyfile!r}: {msg}")

    return ssl_cxt

