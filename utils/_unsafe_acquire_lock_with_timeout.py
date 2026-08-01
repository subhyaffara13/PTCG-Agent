
def _unsafe_acquire_lock_with_timeout(lock: Lock, timeout: float | None = None) -> None:
    """Acquire a threading.Lock with timeout without automatic release (unsafe).

    This function acquires a lock with timeout support but does NOT automatically
    release it. The caller is responsible for releasing the lock explicitly.
    Use this only when you need manual control over lock lifetime.

    Args:
        lock: The threading.Lock object to acquire
        timeout: Timeout in seconds. If None, uses _DEFAULT_TIMEOUT.
                - Use _BLOCKING (-1.0) for infinite wait
                - Use _NON_BLOCKING (0.0) for immediate return
                - Use positive value for finite timeout

    Raises:
        LockTimeoutError: If the lock cannot be acquired within the timeout period

    Warning:
        This is an "unsafe" function because it does not automatically release
        the lock. Always call lock.release() when done, preferably in a try/finally
        block or use the safe _acquire_lock_with_timeout context manager instead.

    Example:
        lock = Lock()
        try:
            _unsafe_acquire_lock_with_timeout(lock, timeout=30.0)
            # Critical section - lock is held
            perform_critical_operation()
        finally:
            lock.release()  # Must manually release!
    """
    _timeout: float = timeout if timeout is not None else _DEFAULT_TIMEOUT
    if not lock.acquire(timeout=_timeout):
        raise exceptions.LockTimeoutError(lock, _timeout)

