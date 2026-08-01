
def parseNameMarker(state: StateBlock, startLine: int) -> tuple[int, str]:
    """Parse field name: `:name:`

    :returns: position after name marker, name text
    """
    start = state.bMarks[startLine] + state.tShift[startLine]
    pos = start
    maximum = state.eMarks[startLine]

    # marker should have at least 3 chars (colon + character + colon)
    if pos + 2 >= maximum:
        return -1, ""

    # first character should be ':'
    if state.src[pos] != ":":
        return -1, ""

    # scan name length
    name_length = 1
    found_close = False
    for ch in state.src[pos + 1 :]:
        if ch == "\n":
            break
        if ch == ":":
            # TODO backslash escapes
            found_close = True
            break
        name_length += 1

    if not found_close:
        return -1, ""

    # get name
    name_text = state.src[pos + 1 : pos + name_length]

    # name should contain at least one character
    if not name_text.strip():
        return -1, ""

    return pos + name_length + 1, name_text

