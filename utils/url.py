
def url(value: str) -> bool:
    """Valid URL (validation uses :obj:`urllib.parse`).
    For maximum compatibility please make sure to include a ``scheme`` prefix
    in your URL (e.g. ``http://``).
    """
    from urllib.parse import urlparse

    try:
        parts = urlparse(value)
        if not parts.scheme:
            _logger.warning(
                "For maximum compatibility please make sure to include a "
                "`scheme` prefix in your URL (e.g. 'http://'). "
                f"Given value: {value}"
            )
            if not (value.startswith("/") or value.startswith("\\") or "@" in value):
                parts = urlparse(f"http://{value}")

        return bool(parts.scheme and parts.netloc)
    except Exception:
        return False

