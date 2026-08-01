
def _normalize_media_type(content_type: str) -> str:
    """Return the bare media type per RFC 7231: strip params, trim, lowercase."""
    if not content_type:
        return ""
    return content_type.split(";", 1)[0].strip().lower()

