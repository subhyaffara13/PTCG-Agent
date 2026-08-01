
def _read_field_unescaped_from_msg(msg: Message, field: str) -> str | None:
    """Read Message header field and apply rfc822_unescape."""
    value = _read_field_from_msg(msg, field)
    if value is None:
        return value
    return rfc822_unescape(value)

