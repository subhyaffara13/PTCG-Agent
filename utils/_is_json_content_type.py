
def _is_json_content_type(content_type: str) -> bool:
    """True iff the body should be parsed as JSON."""
    return _normalize_media_type(content_type) == "application/json"

