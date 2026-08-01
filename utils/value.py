
def value(raw: str) -> _Item:
    """Parse a simple value from a string.

    :Example:

    >>> value("1")
    1
    >>> value("true")
    True
    >>> value("[1, 2, 3]")
    [1, 2, 3]
    """
    parser = Parser(raw)
    v = parser._parse_value()
    if not parser.end():
        raise parser.parse_error(UnexpectedCharError, char=parser._current)
    return v


def value(key: str) -> float:
    """
    Value in physical_constants indexed by key.

    Parameters
    ----------
    key : str
        Key in dictionary `physical_constants`

    Returns
    -------
    value : float
        Value in `physical_constants` corresponding to `key`

    Examples
    --------
    >>> from scipy import constants
    >>> constants.value('elementary charge')
    1.602176634e-19

    """
    _check_obsolete(key)
    return physical_constants[key][0]

