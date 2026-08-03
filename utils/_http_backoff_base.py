import time

def _http_backoff_base(
    method: HTTP_METHOD_T,
    url: str,
    *,
    max_retries: int = 5,
    base_wait_time: float = 1,
    max_wait_time: float = 8,
    retry_on_exceptions: type[Exception] | tuple[type[Exception], ...] = _DEFAULT_RETRY_ON_EXCEPTIONS,
    retry_on_status_codes: int | tuple[int, ...] = _DEFAULT_RETRY_ON_STATUS_CODES,
    stream: bool = False,
    **kwargs,
) -> Generator[httpx.Response, None, None]:
    """Internal implementation of HTTP backoff logic shared between `http_backoff` and `http_stream_backoff`."""
    if isinstance(retry_on_exceptions, type):  # Tuple from single exception type
        retry_on_exceptions = (retry_on_exceptions,)

    if isinstance(retry_on_status_codes, int):  # Tuple from single status code
        retry_on_status_codes = (retry_on_status_codes,)

    nb_tries = 0
    sleep_time = base_wait_time
    ratelimit_reset: int | None = None  # seconds to wait for rate limit reset if 429 response

    # If `data` is used and is a file object (or any IO), it will be consumed on the
    # first HTTP request. We need to save the initial position so that the full content
    # of the file is re-sent on http backoff. See warning tip in docstring.
    io_obj_initial_pos = None
    if "data" in kwargs and isinstance(kwargs["data"], (io.IOBase, SliceFileObj)):
        io_obj_initial_pos = kwargs["data"].tell()

    client = get_session()
    while True:
        nb_tries += 1
        ratelimit_reset = None
        try:
            # If `data` is used and is a file object (or any IO), set back cursor to
            # initial position.
            if io_obj_initial_pos is not None:
                kwargs["data"].seek(io_obj_initial_pos)

            # Perform request and handle response
            def _should_retry(response: httpx.Response) -> bool:
                """Handle response and return True if should retry, False if should return/yield."""
                nonlocal ratelimit_reset

                if response.status_code not in retry_on_status_codes:
                    return False  # Success, don't retry

                # Wrong status code returned (HTTP 503 for instance)
                logger.warning(f"HTTP Error {response.status_code} thrown while requesting {method} {url}")
                if nb_tries > max_retries:
                    hf_raise_for_status(response)  # Will raise uncaught exception
                    # Return/yield response to avoid infinite loop in the corner case where the
                    # user ask for retry on a status code that doesn't raise_for_status.
                    return False  # Don't retry, return/yield response

                # get rate limit reset time from headers if 429 response
                if response.status_code == 429:
                    ratelimit_info = parse_ratelimit_headers(response.headers)
                    if ratelimit_info is not None:
                        ratelimit_reset = ratelimit_info.reset_in_seconds

                return True  # Should retry

            if stream:
                with client.stream(method=method, url=url, **kwargs) as response:
                    if not _should_retry(response):
                        yield response
                        return
            else:
                response = client.request(method=method, url=url, **kwargs)
                if not _should_retry(response):
                    yield response
                    return

        except retry_on_exceptions as err:
            logger.warning(f"'{err}' thrown while requesting {method} {url}")

            if isinstance(err, httpx.ConnectError):
                close_session()  # In case of SSLError it's best to close the shared httpx.Client objects

            if nb_tries > max_retries:
                raise err

        if ratelimit_reset is not None:
            actual_sleep = float(ratelimit_reset) + 1  # +1s to avoid rounding issues
            logger.warning(f"Rate limited. Waiting {actual_sleep}s before retry [Retry {nb_tries}/{max_retries}].")
        else:
            actual_sleep = sleep_time
            logger.warning(f"Retrying in {actual_sleep}s [Retry {nb_tries}/{max_retries}].")

        time.sleep(actual_sleep)

        # Update sleep time for next retry
        sleep_time = min(max_wait_time, sleep_time * 2)  # Exponential backoff

