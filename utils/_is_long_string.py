
def _is_long_string(string_token: str) -> bool:
    """Is this string token a "longstring" (is it triple-quoted)?

    Long strings are triple-quoted as defined in
    https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals

    This function only checks characters up through the open quotes.  Because it's meant
    to be applied only to tokens that represent string literals, it doesn't bother to
    check for close-quotes (demonstrating that the literal is a well-formed string).

    Args:
        string_token: The string token to be parsed.

    Returns:
        A boolean representing whether this token matches a longstring
        regex.
    """
    return bool(
        SINGLE_QUOTED_REGEX.match(string_token)
        or DOUBLE_QUOTED_REGEX.match(string_token)
    )

