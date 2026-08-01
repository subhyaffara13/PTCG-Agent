
def hub_retry(max_attempts: int = 5, wait_before_retry: float | None = 2):
    """
    To decorate tests that download from the Hub. They can fail due to a
    variety of network issues such as timeouts, connection resets, etc.

    Uses exponential backoff starting from `wait_before_retry`.

    Args:
        max_attempts (`int`, *optional*, defaults to 5):
            The maximum number of attempts to retry the flaky test.
        wait_before_retry (`float`, *optional*, defaults to 2):
            If provided, the initial delay in seconds before the first retry.
            Subsequent retries use exponential backoff with jitter.
    """
    from .utils.generic import retry

    return retry(
        max_retries=max_attempts,
        initial_delay=wait_before_retry or 0,
        jitter=wait_before_retry is not None,
        exceptions=(httpx.HTTPError,),
    )

