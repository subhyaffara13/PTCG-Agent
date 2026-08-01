
def wcswidth(s: str) -> int:
    """Determine how many columns are needed to display a string in a terminal.

    Returns -1 if the string contains non-printable characters.
    """
    width = 0
    for c in unicodedata.normalize("NFC", s):
        wc = wcwidth(c)
        if wc < 0:
            return -1
        width += wc
    return width

