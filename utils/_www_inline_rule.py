
def _www_inline_rule(state: StateInline, silent: bool) -> bool:
    """Match ``www.`` autolinks as an inline rule (trigger char: ``w``)."""
    if state.linkLevel > 0:
        return False

    pos = state.pos
    src = state.src

    # Quick check: must be 'w' and form "www."
    if src[pos] != "w":
        return False
    if pos + 4 > state.posMax or src[pos : pos + 4] != "www.":
        return False

    # Check preceding character (from pending text or start-of-line).
    if state.pending:
        preceding = state.pending[-1]
        if not check_prev(preceding):
            return False
    elif pos > 0:
        preceding = src[pos - 1]
        if not check_prev(preceding):
            return False

    result = match_www(src[pos : state.posMax])
    if result is None:
        return False

    url, length = result
    label = src[pos : pos + length]

    if silent:
        return True

    full_url = state.md.normalizeLink(url)
    if not state.md.validateLink(full_url):
        return False

    token = state.push("link_open", "a", 1)
    token.attrs = {"href": full_url}
    token.markup = "autolink"
    token.info = "auto"

    token = state.push("text", "", 0)
    token.content = state.md.normalizeLinkText(label)

    token = state.push("link_close", "a", -1)
    token.markup = "autolink"
    token.info = "auto"

    state.pos += length
    return True

