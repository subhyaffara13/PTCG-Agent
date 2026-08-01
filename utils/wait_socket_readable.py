
def wait_socket_readable(sock: socket.socket) -> Awaitable[None]:
    """
    .. deprecated:: 4.7.0
       Use :func:`wait_readable` instead.

    Wait until the given socket has data to be read.

    .. warning:: Only use this on raw sockets that have not been wrapped by any higher
        level constructs like socket streams!

    :param sock: a socket object
    :raises ~anyio.ClosedResourceError: if the socket was closed while waiting for the
        socket to become readable
    :raises ~anyio.BusyResourceError: if another task is already waiting for the socket
        to become readable
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    """
    return get_async_backend().wait_readable(sock.fileno())

