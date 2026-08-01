
def convert_ipv6_sockaddr(
    sockaddr: tuple[str, int, int, int] | tuple[str, int],
) -> tuple[str, int]:
    """
    Convert a 4-tuple IPv6 socket address to a 2-tuple (address, port) format.

    If the scope ID is nonzero, it is added to the address, separated with ``%``.
    Otherwise the flow id and scope id are simply cut off from the tuple.
    Any other kinds of socket addresses are returned as-is.

    :param sockaddr: the result of :meth:`~socket.socket.getsockname`
    :return: the converted socket address

    """
    # This is more complicated than it should be because of MyPy
    if isinstance(sockaddr, tuple) and len(sockaddr) == 4:
        host, port, flowinfo, scope_id = sockaddr
        if scope_id:
            # PyPy (as of v7.3.11) leaves the interface name in the result, so
            # we discard it and only get the scope ID from the end
            # (https://foss.heptapod.net/pypy/pypy/-/issues/3938)
            host = host.split("%")[0]

            # Add scope_id to the address
            return f"{host}%{scope_id}", port
        else:
            return host, port
    else:
        return sockaddr

