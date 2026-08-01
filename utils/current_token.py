
def current_token() -> EventLoopToken:
    """
    Return a token object that can be used to call code in the current event loop from
    another thread.

    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    .. versionadded:: 4.11.0

    """
    backend_class = get_async_backend()
    raw_token = backend_class.current_token()
    return EventLoopToken(backend_class, raw_token)

