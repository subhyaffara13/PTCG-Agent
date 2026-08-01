
def format_key_part(part: str) -> str:
    try:
        only_bare_key_chars = BARE_KEY_CHARS.issuperset(part)
    except TypeError:
        raise TypeError(
            f"Invalid mapping key '{part}' of type '{type(part).__qualname__}'."
            " A string is required."
        ) from None

    if part and only_bare_key_chars:
        return part
    return format_string(part, allow_multiline=False)


def format_key_part(part: str) -> str:
    try:
        only_bare_key_chars = BARE_KEY_CHARS.issuperset(part)
    except TypeError:
        raise TypeError(
            f"Invalid mapping key '{part}' of type '{type(part).__qualname__}'."
            " A string is required."
        ) from None

    if part and only_bare_key_chars:
        return part
    return format_string(part, allow_multiline=False)

