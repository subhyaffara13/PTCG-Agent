
def _acquire_lock_with_timeout(
    lock: Lock,
    timeout: float | None = None,
) -> Generator[None, None, None]:
    """Context manager that safely acquires a threading.Lock with timeout and automatically releases it.

    This function provides a safe way to acquire a lock with timeout support, ensuring
    the lock is always released even if an exception occurs during execution.

    Args:
        lock: The threading.Lock object to acquire
        timeout: Timeout in seconds. If None, uses _DEFAULT_TIMEOUT.
                - Use _BLOCKING (-1.0) for infinite wait
                - Use _NON_BLOCKING (0.0) for immediate return
                - Use positive value for finite timeout

    Yields:
        None: Yields control to the caller while holding the lock

    Raises:
        LockTimeoutError: If the lock cannot be acquired within the timeout period

    Example:
        with _acquire_lock_with_timeout(my_lock, timeout=30.0):
            # Critical section - lock is held
            perform_critical_operation()
        # Lock is automatically released here
    """
    _unsafe_acquire_lock_with_timeout(lock, timeout=timeout)

    try:
        yield
    finally:
        lock.release()

