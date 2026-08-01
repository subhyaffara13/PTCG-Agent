
def _read_field_from_msg(msg: Message, field: str) -> str | None:
    """Read Message header field."""
    value = msg[field]
    if value == 'UNKNOWN':
        return None
    return value

