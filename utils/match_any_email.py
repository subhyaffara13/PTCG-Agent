
def match_any_email(
    text: str, pos: int, protocol: str | None
) -> tuple[str, int] | None:
    """Match an email address in *text* starting the local-part scan at *pos*.

    *protocol* is ``"mailto"``, ``"xmpp"``, or ``None`` (bare address).
    Returns ``(url, char_count)`` or ``None``.
    """
    size = len(text)

    # scan local part (before @)
    start_pos = pos
    while pos < size:
        ch = text[pos]
        if ch.isascii() and (ch.isalnum() or ch in _EMAIL_OK):
            pos += 1
            continue
        if ch == "@":
            break
        return None

    if pos == start_pos:
        return None

    # scan domain (after @)
    link_end = pos + 1
    np = 0
    num_slash = 0

    while link_end < size:
        ch = text[link_end]
        if ch.isascii() and ch.isalnum():
            pass
        elif ch == "@":
            if protocol != "xmpp":
                return None
        elif (
            ch == "."
            and link_end < size - 1
            and text[link_end + 1].isascii()
            and text[link_end + 1].isalnum()
        ):
            np += 1
        elif ch == "/" and protocol == "xmpp" and num_slash == 0:
            num_slash += 1
        elif ch != "-" and ch != "_":
            break
        link_end += 1

    if link_end < 2 or np == 0:
        return None
    last_ch = text[link_end - 1]
    if not (last_ch.isascii() and last_ch.isalpha()) and last_ch != ".":
        return None

    url = "mailto:" + text[:link_end] if protocol is None else text[:link_end]

    return url, link_end

