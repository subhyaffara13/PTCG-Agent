
def _get_shared_session_lock() -> asyncio.Lock:
    """Lazily create the shared session lock (must be called within a running event loop).

    WARNING: Do not reset _shared_session_lock to None while any coroutine may be
    executing the session-recovery path; doing so breaks the double-checked locking
    guarantee and can cause duplicate session creation.
    """
    global _shared_session_lock
    if _shared_session_lock is None:
        _shared_session_lock = asyncio.Lock()
    return _shared_session_lock

