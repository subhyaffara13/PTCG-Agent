
def quote_header_value(value: t.Any, allow_token: bool = True) -> str:
    """Add double quotes around a header value. If the header contains only ASCII token
    characters, it will be returned unchanged. If the header contains ``"`` or ``\\``
    characters, they will be escaped with an additional ``\\`` character.

    This is the reverse of :func:`unquote_header_value`.

    :param value: The value to quote. Will be converted to a string.
    :param allow_token: Disable to quote the value even if it only has token characters.

    .. versionchanged:: 3.0
        Passing bytes is not supported.

    .. versionchanged:: 3.0
        The ``extra_chars`` parameter is removed.

    .. versionchanged:: 2.3
        The value is quoted if it is the empty string.

    .. versionadded:: 0.5
    """
    value_str = str(value)

    if not value_str:
        return '""'

    if allow_token:
        token_chars = _token_chars

        if token_chars.issuperset(value_str):
            return value_str

    value_str = value_str.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value_str}"'

