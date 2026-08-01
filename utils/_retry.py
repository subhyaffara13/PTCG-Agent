
def _retry(max_retries: int, sleep_time: float) -> Callable:
    """
    A simple retry wrapper.

    Args:
        max_retries: int, the maximum number of retries.
        sleep_time: float, the time to sleep between retries.
    """

    def wrapper(func: Callable[_P, _R]) -> Callable[_P, _R]:
        def wrapper(*args: _P.args, **kwargs: _P.kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    logger.exception("Error running %s. Retrying...", func.__name__)
                    if i < max_retries - 1:
                        time.sleep(sleep_time)
                    else:
                        raise

        return wrapper

    return wrapper

