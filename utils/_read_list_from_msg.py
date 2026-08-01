
def _read_list_from_msg(msg: Message, field: str) -> list[str] | None:
    """Read Message header field and return all results as list."""
    values = msg.get_all(field, None)
    if values == []:
        return None
    return values

