
def wait_writable(obj: FileDescriptorLike) -> Awaitable[None]:
    """
    Wait until the given object can be written to.

    :param obj: an object with a ``.fileno()`` method or an integer handle
    :raises ~anyio.ClosedResourceError: if the object was closed while waiting for the
        object to become writable
    :raises ~anyio.BusyResourceError: if another task is already waiting for the object
        to become writable
    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    .. seealso:: See the documentation of :func:`wait_readable` for the definition of
       ``obj`` and notes on backend compatibility.

    .. warning:: Don't use this on raw sockets that have been wrapped by any higher
        level constructs like socket streams!

    """
    return get_async_backend().wait_writable(obj)

