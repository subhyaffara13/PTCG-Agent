
def get_sockaddr(
    host: str, port: int, family: socket.AddressFamily
) -> tuple[str, int] | str:
    """Return a fully qualified socket address that can be passed to
    :func:`socket.bind`."""
    if family == af_unix:
        # Absolute path avoids IDNA encoding error when path starts with dot.
        return os.path.abspath(host.partition("://")[2])
    try:
        res = socket.getaddrinfo(
            host, port, family, socket.SOCK_STREAM, socket.IPPROTO_TCP
        )
    except socket.gaierror:
        return host, port
    return res[0][4]  # type: ignore

