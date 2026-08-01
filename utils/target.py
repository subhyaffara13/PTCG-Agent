
def target(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    if is_code_block(state, startLine):
        return False

    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    text = state.src[pos:maximum].strip()
    if not text.startswith("("):
        return False
    if not text.endswith(")="):
        return False
    if not text[1:-2]:
        return False

    if silent:
        return True

    state.line = startLine + 1

    token = state.push("myst_target", "", 0)
    token.attrSet("class", "myst-target")
    token.content = text[1:-2]
    token.map = [startLine, state.line]

    return True

