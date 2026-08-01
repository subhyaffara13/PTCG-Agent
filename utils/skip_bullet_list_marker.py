
def skipBulletListMarker(state: StateBlock, startLine: int) -> int:
    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    try:
        marker = state.src[pos]
    except IndexError:
        return -1
    pos += 1

    if marker not in ("*", "-", "+"):
        return -1

    if pos < maximum:
        ch = state.src[pos]

        if not isStrSpace(ch):
            # " -test " - is not a list item
            return -1

    return pos

