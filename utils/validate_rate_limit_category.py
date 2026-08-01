
def validate_rate_limit_category(value: Any) -> Optional[str]:
    """Return ``value`` only if it matches a known :class:`RateLimitErrorCategory`.

    Used at duck-typed read sites (StandardLoggingPayload extraction, Prometheus
    labels) to reject `.category` strings set by unrelated third-party exceptions
    — otherwise those would leak into custom-callback payloads and Prometheus
    label cardinality.
    """
    if isinstance(value, RateLimitErrorCategory):
        return value.value
    if isinstance(value, str) and value in _RATE_LIMIT_CATEGORY_VALUES:
        return value
    return None

