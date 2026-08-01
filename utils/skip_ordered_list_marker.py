
def skipOrderedListMarker(state: StateBlock, startLine: int) -> int:
    start = state.bMarks[startLine] + state.tShift[startLine]
    pos = start
    maximum = state.eMarks[startLine]

    # List marker should have at least 2 chars (digit + dot)
    if pos + 1 >= maximum:
        return -1

    ch = state.src[pos]
    pos += 1

    ch_ord = ord(ch)
    # /* 0 */  /* 9 */
    if ch_ord < 0x30 or ch_ord > 0x39:
        return -1

    while True:
        # EOL -> fail
        if pos >= maximum:
            return -1

        ch = state.src[pos]
        pos += 1

        # /* 0 */  /* 9 */
        ch_ord = ord(ch)
        if ch_ord >= 0x30 and ch_ord <= 0x39:
            # List marker should have no more than 9 digits
            # (prevents integer overflow in browsers)
            if pos - start >= 10:
                return -1

            continue

        # found valid marker
        if ch in (")", "."):
            break

        return -1

    if pos < maximum:
        ch = state.src[pos]

        if not isStrSpace(ch):
            # " 1.test " - is not a list item
            return -1

    return pos

