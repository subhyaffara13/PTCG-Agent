
def _next_sync_or_exhausted(it: Any) -> Any:
    """
    Call next(it) from a thread and return _SYNC_ITER_EXHAUSTED on StopIteration.

    asyncio.to_thread re-raises thread exceptions inside a coroutine, where PEP 479
    converts StopIteration to RuntimeError before any except clause can catch it.
    Returning a sentinel instead keeps StopIteration out of the coroutine boundary.
    """
    try:
        return next(it)
    except StopIteration:
        return _SYNC_ITER_EXHAUSTED

