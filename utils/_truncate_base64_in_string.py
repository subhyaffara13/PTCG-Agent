
def _truncate_base64_in_string(value: str) -> str:
    """Replace long base64 data-URI payloads in a string with a size placeholder."""
    if MAX_BASE64_LENGTH_FOR_LOGGING <= 0:
        return value
    return _DATA_URI_RE.sub(_base64_data_uri_replacer, value)

