
def wait_socket_writable(sock: socket.socket) -> Awaitable[None]:
    """
    .. deprecated:: 4.7.0
       Use :func:`wait_writable` instead.

    Wait until the given socket can be written to.

    This does **NOT** work on Windows when using the asyncio backend with a proactor
    event loop (default on py3.8+).

    .. warning:: Only use this on raw sockets that have not been wrapped by any higher
        level constructs like socket streams!

    :param sock: a socket object
    :raises ~anyio.ClosedResourceError: if the socket was closed while waiting for the
        socket to become writable
    :raises ~anyio.BusyResourceError: if another task is already waiting for the socket
        to become writable
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    """
    return get_async_backend().wait_writable(sock.fileno())

