
def _create_autolink(
    state: StateInline,
    bscan_len: int,
    total_len: int,
    url: str,
    text: str,
) -> bool:
    """Emit ``link_open`` / ``text`` / ``link_close`` tokens.

    *bscan_len* characters are trimmed from the end of ``state.pending``
    (the back-scanned protocol or local part).  The parser position is
    then advanced by ``total_len - bscan_len`` characters.
    """
    if bscan_len:
        state.pending = state.pending[:-bscan_len]

    full_url = state.md.normalizeLink(url)
    if not state.md.validateLink(full_url):
        return False

    token = state.push("link_open", "a", 1)
    token.attrs = {"href": full_url}
    token.markup = "autolink"
    token.info = "auto"

    token = state.push("text", "", 0)
    token.content = state.md.normalizeLinkText(text)

    token = state.push("link_close", "a", -1)
    token.markup = "autolink"
    token.info = "auto"

    state.pos += total_len - bscan_len
    return True

