
def trim_front(strings: list[str]) -> list[str]:
    """
    Trims leading spaces evenly among all strings.

    Examples
    --------
    >>> trim_front([" a", " b"])
    ['a', 'b']

    >>> trim_front([" a", " "])
    ['a', '']
    """
    if not strings:
        return strings
    smallest_leading_space = min(len(x) - len(x.lstrip()) for x in strings)
    if smallest_leading_space > 0:
        strings = [x[smallest_leading_space:] for x in strings]
    return strings

