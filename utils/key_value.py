
def key_value(src: str) -> tuple[Key, _Item]:
    """Parse a key-value pair from a string.

    :Example:

    >>> key_value("foo = 1")
    (Key('foo'), 1)
    """
    return Parser(src)._parse_key_value()

