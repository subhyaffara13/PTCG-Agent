
def parseLinkTitle(
    string: str, start: int, maximum: int, prev_state: _State | None = None
) -> _State:
    """Parse link title within `str` in [start, max] range,
    or continue previous parsing if `prev_state` is defined (equal to result of last execution).
    """
    pos = start
    state = _State()

    if prev_state is not None:
        # this is a continuation of a previous parseLinkTitle call on the next line,
        # used in reference links only
        state.str = prev_state.str
        state.marker = prev_state.marker
    else:
        if pos >= maximum:
            return state

        marker = charCodeAt(string, pos)

        # /* " */  /* ' */  /* ( */
        if marker != 0x22 and marker != 0x27 and marker != 0x28:
            return state

        start += 1
        pos += 1

        # if opening marker is "(", switch it to closing marker ")"
        if marker == 0x28:
            marker = 0x29

        state.marker = marker

    while pos < maximum:
        code = charCodeAt(string, pos)
        if code == state.marker:
            state.pos = pos + 1
            state.str += unescapeAll(string[start:pos])
            state.ok = True
            return state
        elif code == 0x28 and state.marker == 0x29:  # /* ( */  /* ) */
            return state
        elif code == 0x5C and pos + 1 < maximum:  # /* \ */
            pos += 1

        pos += 1

    # no closing marker found, but this link title may continue on the next line (for references)
    state.can_continue = True
    state.str += unescapeAll(string[start:pos])
    return state

