
def getnameinfo(sockaddr: IPSockAddrType, flags: int = 0) -> Awaitable[tuple[str, str]]:
    """
    Look up the host name of an IP address.

    :param sockaddr: socket address (e.g. (ipaddress, port) for IPv4)
    :param flags: flags to pass to upstream ``getnameinfo()``
    :return: a tuple of (host name, service name)
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    .. seealso:: :func:`socket.getnameinfo`

    """
    return get_async_backend().getnameinfo(sockaddr, flags)

