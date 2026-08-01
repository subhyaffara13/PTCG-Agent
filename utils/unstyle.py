
def unstyle(text: str) -> str:
    """Removes ANSI styling information from a string.  Usually it's not
    necessary to use this function as Click's echo function will
    automatically remove styling if necessary.

    .. versionadded:: 2.0

    :param text: the text to remove style information from.
    """
    return strip_ansi(text)

