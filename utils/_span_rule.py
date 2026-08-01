
def _span_rule(state: StateInline, silent: bool) -> bool:
    if state.src[state.pos] != "[":
        return False

    maximum = state.posMax
    labelStart = state.pos + 1
    labelEnd = state.md.helpers.parseLinkLabel(state, state.pos, False)

    # parser failed to find ']', so it's not a valid span
    if labelEnd < 0:
        return False

    pos = labelEnd + 1

    # check not at end of inline
    if pos >= maximum:
        return False

    try:
        new_pos, attrs = parse(state.src[pos:])
    except ParseError:
        return False

    pos += new_pos + 1

    if not silent:
        state.pos = labelStart
        state.posMax = labelEnd
        token = state.push("span_open", "span", 1)
        token.attrs = attrs  # type: ignore[assignment]
        state.md.inline.tokenize(state)
        token = state.push("span_close", "span", -1)

    state.pos = pos
    state.posMax = maximum
    return True

