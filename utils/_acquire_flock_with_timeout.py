
def _acquire_flock_with_timeout(
    flock: BaseFileLock,
    timeout: float | None = None,
) -> Generator[None, None, None]:
    """Context manager that safely acquires a FileLock with timeout and automatically releases it.

    This function provides a safe way to acquire a file lock with timeout support, ensuring
    the lock is always released even if an exception occurs during execution.

    Args:
        flock: The FileLock object to acquire
        timeout: Timeout in seconds. If None, uses _DEFAULT_TIMEOUT.
                - Use _BLOCKING (-1.0) for infinite wait
                - Use _NON_BLOCKING (0.0) for immediate return
                - Use positive value for finite timeout

    Yields:
        None: Yields control to the caller while holding the file lock

    Raises:
        FileLockTimeoutError: If the file lock cannot be acquired within the timeout period

    Example:
        flock = FileLock("/tmp/my_process.lock")
        with _acquire_flock_with_timeout(flock, timeout=30.0):
            # Critical section - file lock is held
            perform_exclusive_file_operation()
        # File lock is automatically released here
    """
    _unsafe_acquire_flock_with_timeout(flock, timeout=timeout)

    try:
        yield
    finally:
        flock.release()

