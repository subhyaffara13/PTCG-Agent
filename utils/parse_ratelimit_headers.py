
def parse_ratelimit_headers(headers: Mapping[str, str]) -> RateLimitInfo | None:
    """Parse rate limit information from HTTP response headers.

    Follows IETF draft: https://www.ietf.org/archive/id/draft-ietf-httpapi-ratelimit-headers-09.html
    Only a subset is implemented.

    Example:
    ```python
    >>> from huggingface_hub.utils import parse_ratelimit_headers
    >>> headers = {
    ...     "ratelimit": '"api";r=0;t=55',
    ...     "ratelimit-policy": '"fixed window";"api";q=500;w=300',
    ... }
    >>> info = parse_ratelimit_headers(headers)
    >>> info.remaining
    0
    >>> info.reset_in_seconds
    55
    ```
    """

    ratelimit: str | None = None
    policy: str | None = None
    for key in headers:
        lower_key = key.lower()
        if lower_key == "ratelimit":
            ratelimit = headers[key]
        elif lower_key == "ratelimit-policy":
            policy = headers[key]

    if not ratelimit:
        return None

    match = _RATELIMIT_REGEX.search(ratelimit)
    if not match:
        return None

    resource_type = match.group("resource_type")
    remaining = int(match.group("r"))
    reset_in_seconds = int(match.group("t"))

    limit: int | None = None
    window_seconds: int | None = None

    if policy:
        policy_match = _RATELIMIT_POLICY_REGEX.search(policy)
        if policy_match:
            limit = int(policy_match.group("q"))
            window_seconds = int(policy_match.group("w"))

    return RateLimitInfo(
        resource_type=resource_type,
        remaining=remaining,
        reset_in_seconds=reset_in_seconds,
        limit=limit,
        window_seconds=window_seconds,
    )

