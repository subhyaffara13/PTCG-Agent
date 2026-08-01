
def charStrAt(src: str, pos: int) -> str | None:
    """
    Returns the Unicode value of the character at the specified location.

    @param - index The zero-based index of the desired character.
    If there is no character at the specified index, NaN is returned.

    This was added for compatibility with python
    """
    try:
        return src[pos]
    except IndexError:
        return None

