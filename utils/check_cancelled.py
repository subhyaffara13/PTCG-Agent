
def check_cancelled() -> None:
    """
    Check if the cancel scope of the host task's running the current worker thread has
    been cancelled.

    If the host task's current cancel scope has indeed been cancelled, the
    backend-specific cancellation exception will be raised.

    :raises RuntimeError: if the current thread was not spawned by
        :func:`.to_thread.run_sync`

    """
    try:
        token: EventLoopToken = threadlocals.current_token
    except AttributeError:
        raise NoEventLoopError(
            "This function can only be called inside an AnyIO worker thread"
        ) from None

    token.backend_class.check_cancelled()

