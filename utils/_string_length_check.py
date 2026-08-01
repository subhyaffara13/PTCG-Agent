
def _string_length_check(text: str | bytes | bytearray) -> None:
    if MAX_STRING_LENGTH is not None and len(text) > MAX_STRING_LENGTH:
        msg = "too many characters in string"
        raise ValueError(msg)

