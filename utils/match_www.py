
def match_www(text: str) -> tuple[str, int] | None:
    """Match a bare ``www.`` URL at the start of *text*.

    Returns ``(url_with_scheme, char_count)`` or ``None``.
    """
    if not text.startswith("www."):
        return None

    link_end = _check_domain(text[4:], False)
    if link_end is None:
        return None
    # link_end is offset from position 4
    link_end += 4

    # extend to the end of non-space characters
    while link_end < len(text) and not _isspace(text[link_end]):
        link_end += 1

    link_end = _autolink_delim(text, link_end)

    matched = text[:link_end]
    url = "http://" + matched
    return url, len(matched)

