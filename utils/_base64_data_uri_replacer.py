
def _base64_data_uri_replacer(match: re.Match) -> str:
    """Replace a single base64 data-URI match with a size placeholder if too long."""
    mime_type = match.group(1)
    payload = match.group(2)
    if len(payload) <= MAX_BASE64_LENGTH_FOR_LOGGING:
        return match.group(0)
    size_str = _format_base64_size(len(payload))
    return f"data:{mime_type};base64,[base64_data truncated: {size_str}]"

