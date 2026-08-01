
def autolink(state: StateInline, silent: bool) -> bool:
    pos = state.pos

    if state.src[pos] != "<":
        return False

    start = state.pos
    maximum = state.posMax

    while True:
        pos += 1
        if pos >= maximum:
            return False

        ch = state.src[pos]

        if ch == "<":
            return False
        if ch == ">":
            break

    url = state.src[start + 1 : pos]

    if AUTOLINK_RE.search(url) is not None:
        fullUrl = state.md.normalizeLink(url)
        if not state.md.validateLink(fullUrl):
            return False

        if not silent:
            token = state.push("link_open", "a", 1)
            token.attrs = {"href": fullUrl}
            token.markup = "autolink"
            token.info = "auto"

            token = state.push("text", "", 0)
            token.content = state.md.normalizeLinkText(url)

            token = state.push("link_close", "a", -1)
            token.markup = "autolink"
            token.info = "auto"

        state.pos += len(url) + 2
        return True

    if EMAIL_RE.search(url) is not None:
        fullUrl = state.md.normalizeLink("mailto:" + url)
        if not state.md.validateLink(fullUrl):
            return False

        if not silent:
            token = state.push("link_open", "a", 1)
            token.attrs = {"href": fullUrl}
            token.markup = "autolink"
            token.info = "auto"

            token = state.push("text", "", 0)
            token.content = state.md.normalizeLinkText(url)

            token = state.push("link_close", "a", -1)
            token.markup = "autolink"
            token.info = "auto"

        state.pos += len(url) + 2
        return True

    return False

