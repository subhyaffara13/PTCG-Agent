
def retry_on_error(func: Callable[[], Any], max_wait: float = 1.0) -> None:
    """Retry callback with exponential backoff when it raises OSError.

    If the function still generates an error after max_wait seconds, propagate
    the exception.

    This can be effective against random file system operation failures on
    Windows.
    """
    t0 = time.time()
    wait_time = 0.01
    while True:
        try:
            func()
            return
        except OSError:
            wait_time = min(wait_time * 2, t0 + max_wait - time.time())
            if wait_time <= 0.01:
                # Done enough waiting, the error seems persistent.
                raise
            time.sleep(wait_time)

