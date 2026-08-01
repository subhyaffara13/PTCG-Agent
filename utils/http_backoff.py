
def http_backoff(
    method: HTTP_METHOD_T,
    url: str,
    *,
    max_retries: int = 5,
    base_wait_time: float = 1,
    max_wait_time: float = 8,
    retry_on_exceptions: type[Exception] | tuple[type[Exception], ...] = _DEFAULT_RETRY_ON_EXCEPTIONS,
    retry_on_status_codes: int | tuple[int, ...] = _DEFAULT_RETRY_ON_STATUS_CODES,
    **kwargs,
) -> httpx.Response:
    """Wrapper around httpx to retry calls on an endpoint, with exponential backoff.

    Endpoint call is retried on exceptions (ex: connection timeout, proxy error,...)
    and/or on specific status codes (ex: service unavailable). If the call failed more
    than `max_retries`, the exception is thrown or `raise_for_status` is called on the
    response object.

    Re-implement mechanisms from the `backoff` library to avoid adding an external
    dependencies to `hugging_face_hub`. See https://github.com/litl/backoff.

    Args:
        method (`Literal["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"]`):
            HTTP method to perform.
        url (`str`):
            The URL of the resource to fetch.
        max_retries (`int`, *optional*, defaults to `5`):
            Maximum number of retries, defaults to 5 (no retries).
        base_wait_time (`float`, *optional*, defaults to `1`):
            Duration (in seconds) to wait before retrying the first time.
            Wait time between retries then grows exponentially, capped by
            `max_wait_time`.
        max_wait_time (`float`, *optional*, defaults to `8`):
            Maximum duration (in seconds) to wait before retrying.
        retry_on_exceptions (`type[Exception]` or `tuple[type[Exception]]`, *optional*):
            Define which exceptions must be caught to retry the request. Can be a single type or a tuple of types.
            By default, retry on `httpx.TimeoutException`, `httpx.NetworkError` and `httpx.RemoteProtocolError`.
        retry_on_status_codes (`int` or `tuple[int]`, *optional*, defaults to `(429, 500, 502, 503, 504)`):
            Define on which status codes the request must be retried. By default, retries
            on rate limit (429) and server errors (5xx).
        **kwargs (`dict`, *optional*):
            kwargs to pass to `httpx.request`.

    Example:
    ```
    >>> from huggingface_hub.utils import http_backoff

    # Same usage as "httpx.request".
    >>> response = http_backoff("GET", "https://www.google.com")
    >>> response.raise_for_status()

    # If you expect a Gateway Timeout from time to time
    >>> http_backoff("PUT", upload_url, data=data, retry_on_status_codes=504)
    >>> response.raise_for_status()
    ```

    > [!WARNING]
    > When using `requests` it is possible to stream data by passing an iterator to the
    > `data` argument. On http backoff this is a problem as the iterator is not reset
    > after a failed call. This issue is mitigated for file objects or any IO streams
    > by saving the initial position of the cursor (with `data.tell()`) and resetting the
    > cursor between each call (with `data.seek()`). For arbitrary iterators, http backoff
    > will fail. If this is a hard constraint for you, please let us know by opening an
    > issue on [Github](https://github.com/huggingface/huggingface_hub).
    """
    return next(
        _http_backoff_base(
            method=method,
            url=url,
            max_retries=max_retries,
            base_wait_time=base_wait_time,
            max_wait_time=max_wait_time,
            retry_on_exceptions=retry_on_exceptions,
            retry_on_status_codes=retry_on_status_codes,
            stream=False,
            **kwargs,
        )
    )

