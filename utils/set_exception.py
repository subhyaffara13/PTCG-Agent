
def set_exception(
    fut: "asyncio.Future[_T] | ErrorableProtocol",
    exc: BaseException,
    exc_cause: BaseException = _EXC_SENTINEL,
) -> None:
    """Set future exception.

    If the future is marked as complete, this function is a no-op.

    :param exc_cause: An exception that is a direct cause of ``exc``.
                      Only set if provided.
    """
    if asyncio.isfuture(fut) and fut.done():
        return

    exc_is_sentinel = exc_cause is _EXC_SENTINEL
    exc_causes_itself = exc is exc_cause
    if not exc_is_sentinel and not exc_causes_itself:
        exc.__cause__ = exc_cause

    fut.set_exception(exc)

