
def block_break(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    if is_code_block(state, startLine):
        return False

    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    marker = state.src[pos]
    pos += 1

    # Check block marker
    if marker != "+":
        return False

    # markers can be mixed with spaces, but there should be at least 3 of them

    cnt = 1
    while pos < maximum:
        ch = state.src[pos]
        if ch != marker and ch not in ("\t", " "):
            break
        if ch == marker:
            cnt += 1
        pos += 1

    if cnt < 3:
        return False

    if silent:
        return True

    state.line = startLine + 1

    token = state.push("myst_block_break", "hr", 0)
    token.attrSet("class", "myst-block")
    token.content = state.src[pos:maximum].strip()
    token.map = [startLine, state.line]
    token.markup = marker * cnt

    return True

