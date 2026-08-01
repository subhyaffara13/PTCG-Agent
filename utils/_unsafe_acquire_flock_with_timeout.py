
def _unsafe_acquire_flock_with_timeout(
    flock: BaseFileLock,
    timeout: float | None,
) -> None:
    """Acquire a FileLock with timeout without automatic release (unsafe).

    This function acquires a file lock with timeout support but does NOT automatically
    release it. The caller is responsible for releasing the lock explicitly.
    Use this only when you need manual control over lock lifetime.

    Args:
        flock: The FileLock object to acquire
        timeout: Timeout in seconds. If None, uses _DEFAULT_TIMEOUT.
                - Use _BLOCKING (-1.0) for infinite wait
                - Use _NON_BLOCKING (0.0) for immediate return
                - Use positive value for finite timeout

    Raises:
        FileLockTimeoutError: If the file lock cannot be acquired within the timeout period

    Warning:
        This is an "unsafe" function because it does not automatically release
        the lock. Always call flock.release() when done, preferably in a try/finally
        block or use the safe _acquire_flock_with_timeout context manager instead.

    Example:
        flock = FileLock("/tmp/my_process.lock")
        try:
            _unsafe_acquire_flock_with_timeout(flock, timeout=30.0)
            # Critical section - file lock is held
            perform_exclusive_file_operation()
        finally:
            flock.release()  # Must manually release!
    """
    _timeout: float = timeout if timeout is not None else _DEFAULT_TIMEOUT
    try:
        _ = flock.acquire(timeout=_timeout)
    except Timeout as err:
        raise exceptions.FileLockTimeoutError(flock, _timeout) from err

