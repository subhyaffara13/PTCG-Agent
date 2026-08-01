
def _scan_balanced_value_end(text: str, start: int) -> int:
    """
    Given ``text[start]`` is ``[``, ``{``, ``'`` or ``"``, return the index
    just past the matching close, accounting for nested brackets and
    quoted strings (with escape sequences). Returns ``-1`` if the
    structure is unterminated.

    Implemented iteratively (no self-recursion): the bracket scanner
    inlines a quote-skip helper rather than re-entering itself, since
    JSON-style values cannot contain another bracket *as a first char*
    inside a quoted string — only the quote-skip case can occur.
    """
    n = len(text)
    if start >= n:
        return -1
    first = text[start]
    if first in ("'", '"'):
        return _scan_quoted_string_end(text, start, first)
    if first == "[":
        close = "]"
    elif first == "{":
        close = "}"
    else:
        return -1
    depth = 0
    i = start
    while i < n:
        c = text[i]
        if c in ("'", '"'):
            end = _scan_quoted_string_end(text, i, c)
            if end == -1:
                return -1
            i = end
            continue
        if c == first:
            depth += 1
        elif c == close:
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    return -1

