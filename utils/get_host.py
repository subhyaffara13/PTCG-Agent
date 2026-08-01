
def get_host(
    environ: WSGIEnvironment, trusted_hosts: t.Collection[str] | None = None
) -> str:
    """Get and validate a request's ``host:port`` based on the values in the
    given WSGI environ.

    The ``Host`` header sent by the client is preferred. Otherwise, the server's
    configured address is used. If the server address is a Unix socket, it is
    ignored. The port is omitted if it matches the standard HTTP or HTTPS ports.

    The value is passed through :func:`host_is_trusted`. The host must be made
    up of valid characters, but this does not check validity beyond that. If a
    list of trusted domains is given, the domain must match one.

    :param environ: The WSGI environ.
    :param trusted_hosts: A list of trusted domains to match. These should
        already be IDNA encoded, but will be encoded if needed. The port is
        ignored for this check. If a name starts with a dot it will match as a
        suffix, accepting all subdomains. If empty or ``None``, all domains are
        allowed.

    :return: Host, with port if necessary.
    :raise .SecurityError: If the host is not trusted.

    .. versionchanged:: 3.2
        The characters of the host value are validated. The empty string is no
        longer allowed if no header value is available.

    .. versionchanged:: 3.2
        When using the server address, Unix sockets are ignored.

    .. versionchanged:: 3.1.3
        If ``SERVER_NAME`` is IPv6, it is wrapped in ``[]``.
    """
    return _sansio_utils.get_host(
        environ["wsgi.url_scheme"],
        environ.get("HTTP_HOST"),
        _get_server(environ),
        trusted_hosts,
    )


def get_host(
    scheme: str,
    host_header: str | None,
    server: tuple[str, int | None] | None = None,
    trusted_hosts: t.Collection[str] | None = None,
) -> str:
    """Get and validate a request's ``host:port`` based on the given values.

    The ``Host`` header sent by the client is preferred. Otherwise, the server's
    configured address is used. The port is omitted if it matches the standard
    HTTP or HTTPS ports.

    The value is passed through :func:`host_is_trusted`. The host must be made
    up of valid characters, but this does not check validity beyond that. If a
    list of trusted domains is given, the domain must match one.

    If the host header is not available, such as for HTTP/0.9 and 1.0, or it has
    invalid characters, the empty string is returned. Subdomain and host
    routing, and external URL building, will not work in these cases.

    :param scheme: The protocol of the request. Used to omit the standard ports
        80 and 443.
    :param host_header: The ``Host`` header value.
    :param server: The server's configured address ``(host, port)``. The server
        may be using a Unix socket and give ``(path, None)``; this is ignored as
        it would not produce a useful host value.
    :param trusted_hosts: A list of trusted domains to match. These should
        already be IDNA encoded, but will be encoded if needed. The port is
        ignored for this check. If a name starts with a dot it will match as a
        suffix, accepting all subdomains. If empty or ``None``, all domains are
        allowed.

    :return: Host, with port if necessary.
    :raise .SecurityError: If the host is not trusted.

    .. versionchanged:: 3.1.8
        The empty string is again returned if no host header value is available,
        or if the characters are invalid.

    .. versionchanged:: 3.1.7
        The characters of the host value are validated. The empty string is no
        longer allowed if no header value is available.

    .. versionchanged:: 3.2
        When using the server address, Unix sockets are ignored.

    .. versionchanged:: 3.1.3
        If ``SERVER_NAME`` is IPv6, it is wrapped in ``[]``.
    """
    if host_header is not None:
        host = host_header
    # The port server[1] will be None for a Unix socket. Ignore in that case.
    elif server is not None and server[1] is not None:
        host = server[0]

        # If SERVER_NAME is IPv6, wrap it in [] to match Host header.
        # Check for : because domain or IPv4 can't have that.
        if ":" in host and host[0] != "[":
            host = f"[{host}]"

        host = f"{host}:{server[1]}"
    else:
        # Pass through empty host from HTTP/0.9 and 1.0.
        return ""

    if scheme in {"http", "ws"}:
        host = host.removesuffix(":80")
    elif scheme in {"https", "wss"}:
        host = host.removesuffix(":443")

    if not host_is_trusted(host, trusted_hosts):
        if trusted_hosts:
            raise SecurityError(f"Host {host!r} is not trusted.")

        # Invalid characters, treat as empty.
        return ""

    return host

