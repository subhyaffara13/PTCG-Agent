
def match_http(text: str) -> tuple[str, int] | None:
    """Match an ``http://`` or ``https://`` URL at the start of *text*.

    Returns ``(url, char_count)`` or ``None``.
    """
    if text.startswith("http://"):
        prefix_len = 7
    elif text.startswith("https://"):
        prefix_len = 8
    else:
        return None

    link_end = _check_domain(text[prefix_len:], True)
    if link_end is None:
        return None
    link_end += prefix_len

    while link_end < len(text) and not _isspace(text[link_end]):
        link_end += 1

    link_end = _autolink_delim(text, link_end)

    url = text[:link_end]
    return url, len(url)

