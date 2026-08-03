from typing import Any

def _httpx_follow_relative_redirects_with_backoff(
    method: HTTP_METHOD_T, url: str, *, retry_on_errors: bool = False, **httpx_kwargs
) -> httpx.Response:
    """Perform an HTTP request with backoff and follow relative redirects only.

    Used to fetch HEAD /resolve on repo or bucket files.

    This is useful to follow a redirection to a renamed repository without following redirection to a CDN.

    A backoff mechanism retries the HTTP call on errors (429, 5xx, timeout, network errors).

    Args:
        method (`str`):
            HTTP method, such as 'GET' or 'HEAD'.
        url (`str`):
            The URL of the resource to fetch.
        retry_on_errors (`bool`, *optional*, defaults to `False`):
            Whether to retry on errors. If False, no retry is performed (fast fallback to local cache).
            If True, uses default retry behavior (429, 5xx, timeout, network errors).
        **httpx_kwargs (`dict`, *optional*):
            Params to pass to `httpx.request`.
    """
    # if `retry_on_errors=False`, disable all retries for fast fallback to cache
    no_retry_kwargs: dict[str, Any] = (
        {} if retry_on_errors else {"retry_on_exceptions": (), "retry_on_status_codes": ()}
    )

    while True:
        response = http_backoff(
            method=method,
            url=url,
            **httpx_kwargs,
            follow_redirects=False,
            **no_retry_kwargs,
        )
        hf_raise_for_status(response)

        # Check if response is a relative redirect
        if 300 <= response.status_code <= 399:
            parsed_target = urlparse(response.headers["Location"])
            if parsed_target.netloc == "":
                # Relative redirect -> update URL and retry
                url = urlparse(url)._replace(path=parsed_target.path).geturl()
                continue

        # Break if no relative redirect
        break

    return response

