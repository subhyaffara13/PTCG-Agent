
def parse_list_header(value: str) -> list[str]:
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    :rtype: list
    """
    result: list[str] = []
    for item in _parse_list_header(value):
        if item[:1] == item[-1:] == '"':
            item = unquote_header_value(item[1:-1])
        result.append(item)
    return result


def parse_list_header(value: str) -> list[str]:
    """Parse a header value that consists of a list of comma separated items according
    to `RFC 9110 <https://httpwg.org/specs/rfc9110.html#abnf.extension>`__.

    Surrounding quotes are removed from items, but internal quotes are left for
    future parsing. Empty values are discarded.

    .. code-block:: python

        parse_list_header('token, "quoted value"')
        ['token', 'quoted value']

    This is the reverse of :func:`dump_header`.

    :param value: The header value to parse.

    .. versionchanged:: 3.2
        Quotes and escapes are kept if only part of an item is quoted. Empty
        values are omitted. An empty list is returned if the value contains an
        unclosed quoted string.
    """
    items = []
    item = ""
    escape = False
    quote = False

    for char in value:
        if escape:
            escape = False
            item += char
            continue

        if quote:
            if char == "\\":
                escape = True
            elif char == '"':
                quote = False

            item += char
            continue

        if char == ",":
            items.append(item)
            item = ""
            continue

        if char == '"':
            quote = True

        item += char

    if quote:
        # invalid, unclosed quoted string
        return []

    items.append(item)
    return [
        unquote_header_value(item) for item in (item.strip() for item in items) if item
    ]


def parse_list_header(value):
    """Parse lists as described by RFC 2068 Section 2.

    In particular, parse comma-separated lists where the elements of
    the list may include quoted-strings.  A quoted-string could
    contain a comma.  A non-quoted string could have quotes in the
    middle.  Quotes are removed automatically after parsing.

    It basically works like :func:`parse_set_header` just that items
    may appear multiple times and case sensitivity is preserved.

    The return value is a standard :class:`list`:

    >>> parse_list_header('token, "quoted value"')
    ['token', 'quoted value']

    To create a header from the :class:`list` again, use the
    :func:`dump_header` function.

    :param value: a string with a list header.
    :return: :class:`list`
    :rtype: list
    """
    result = []
    for item in _parse_list_header(value):
        if item[:1] == item[-1:] == '"':
            item = unquote_header_value(item[1:-1])
        result.append(item)
    return result

