
def percent_encoded(string: str, safe: str) -> str:
    """
    Use percent-encoding to quote a string.
    """
    NON_ESCAPED_CHARS = UNRESERVED_CHARACTERS + safe

    # Fast path for strings that don't need escaping.
    if not string.rstrip(NON_ESCAPED_CHARS):
        return string

    return "".join(
        [char if char in NON_ESCAPED_CHARS else PERCENT(char) for char in string]
    )

