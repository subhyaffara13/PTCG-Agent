
def wait_readable(obj: FileDescriptorLike) -> Awaitable[None]:
    """
    Wait until the given object has data to be read.

    On Unix systems, ``obj`` must either be an integer file descriptor, or else an
    object with a ``.fileno()`` method which returns an integer file descriptor. Any
    kind of file descriptor can be passed, though the exact semantics will depend on
    your kernel. For example, this probably won't do anything useful for on-disk files.

    On Windows systems, ``obj`` must either be an integer ``SOCKET`` handle, or else an
    object with a ``.fileno()`` method which returns an integer ``SOCKET`` handle. File
    descriptors aren't supported, and neither are handles that refer to anything besides
    a ``SOCKET``.

    On backends where this functionality is not natively provided (asyncio
    ``ProactorEventLoop`` on Windows), it is provided using a separate selector thread
    which is set to shut down when the interpreter shuts down.

    .. warning:: Don't use this on raw sockets that have been wrapped by any higher
        level constructs like socket streams!

    :param obj: an object with a ``.fileno()`` method or an integer handle
    :raises ~anyio.ClosedResourceError: if the object was closed while waiting for the
        object to become readable
    :raises ~anyio.BusyResourceError: if another task is already waiting for the object
        to become readable
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    """
    return get_async_backend().wait_readable(obj)

