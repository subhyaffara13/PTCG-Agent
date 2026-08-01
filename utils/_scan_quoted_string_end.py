
def _scan_quoted_string_end(text: str, start: int, quote: str) -> int:
    """
    Given ``text[start] == quote`` (``'`` or ``"``), return the index just
    past the matching close quote, honoring backslash escapes. Returns
    ``-1`` if unterminated.
    """
    n = len(text)
    i = start + 1
    while i < n:
        c = text[i]
        if c == "\\":
            i += 2
            continue
        if c == quote:
            return i + 1
        i += 1
    return -1

