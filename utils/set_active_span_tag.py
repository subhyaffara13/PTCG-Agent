
def set_active_span_tag(tag_key: str, tag_value: str) -> bool:
    """
    Best-effort helper to set a tag on the active Datadog span.

    Returns:
        bool: True if a span tag was set, False otherwise.
    """
    if not tag_key or tag_value is None:
        return False

    span = get_active_span()
    if span is None:
        return False

    try:
        if hasattr(span, "set_tag_str"):
            span.set_tag_str(tag_key, str(tag_value))
            return True
        if hasattr(span, "set_tag"):
            span.set_tag(tag_key, str(tag_value))
            return True
    except Exception:
        return False
    return False

