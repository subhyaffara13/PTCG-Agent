
def get_cancelled_exc_class() -> type[BaseException]:
    """
    Return the current async library's cancellation exception class.

    :raises NoEventLoopError: if no supported asynchronous event loop is running in the
        current thread

    """
    return get_async_backend().cancelled_exception_class()

