
def _get_quote_delimiter(string_token: str) -> str:
    """Returns the quote character used to delimit this token string.

    This function checks whether the token is a well-formed string.

    Args:
        string_token: The token to be parsed.

    Returns:
        A string containing solely the first quote delimiter character in the
        given string.

    Raises:
      ValueError: No quote delimiter characters are present.
    """
    match = QUOTE_DELIMITER_REGEX.match(string_token)
    if not match:
        raise ValueError(f"string token {string_token} is not a well-formed string")
    return match.group(2)

