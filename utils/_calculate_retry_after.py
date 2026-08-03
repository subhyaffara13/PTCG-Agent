import random
from typing import Optional, Union

def _calculate_retry_after(
    remaining_retries: int,
    max_retries: int,
    response_headers: Optional[httpx.Headers] = None,
    min_timeout: int = 0,
) -> Union[float, int]:
    retry_after = _get_retry_after_from_exception_header(response_headers)

    # Add some jitter (default JITTER is 0.75 - so upto 0.75s)
    jitter = JITTER * random.random()

    # If the API asks us to wait a certain amount of time (and it's a reasonable amount), just do what it says.
    if retry_after is not None and 0 < retry_after <= 60:
        return retry_after + jitter

    # Calculate exponential backoff
    num_retries = max_retries - remaining_retries
    sleep_seconds = INITIAL_RETRY_DELAY * pow(2.0, num_retries)

    # Make sure sleep_seconds is boxed between min_timeout and MAX_RETRY_DELAY
    sleep_seconds = max(sleep_seconds, min_timeout)
    sleep_seconds = min(sleep_seconds, MAX_RETRY_DELAY)

    return sleep_seconds + jitter

