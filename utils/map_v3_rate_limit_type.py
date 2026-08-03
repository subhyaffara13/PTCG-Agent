from typing import Optional

def map_v3_rate_limit_type(
    v3_value: Optional[str],
) -> Optional[RateLimitType]:
    """
    Map the v3 rate limiter's internal `status["rate_limit_type"]` strings
    onto the public :class:`RateLimitType` enum.

    The v3 limiter uses the literal values ``"requests"``, ``"tokens"``, and
    ``"max_parallel_requests"``. We collapse the last one onto
    :attr:`RateLimitType.CONCURRENT_REQUESTS` because that's the public name
    documented for users and dashboards. Unrecognized values return ``None``
    so the field stays absent rather than carrying garbage downstream.
    """
    if v3_value == "tokens":
        return RateLimitType.TOKENS
    if v3_value == "max_parallel_requests":
        return RateLimitType.CONCURRENT_REQUESTS
    if v3_value == "requests":
        return RateLimitType.REQUESTS
    return None

