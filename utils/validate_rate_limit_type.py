from typing import Any, Optional

def validate_rate_limit_type(value: Any) -> Optional[str]:
    """Return ``value`` only if it matches a known :class:`RateLimitType`.

    See :func:`validate_rate_limit_category` for the rationale.
    """
    if isinstance(value, RateLimitType):
        return value.value
    if isinstance(value, str) and value in _RATE_LIMIT_TYPE_VALUES:
        return value
    return None

