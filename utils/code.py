
def code(func):
    """get the code object for the given function or method

    NOTE: use dill.source.getsource(CODEOBJ) to get the source code
    """
    if ismethod(func): func = func.__func__
    if isfunction(func): func = func.__code__
    if istraceback(func): func = func.tb_frame
    if isframe(func): func = func.f_code
    if iscode(func): return func
    return


def code(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    LOGGER.debug("entering code: %s, %s, %s, %s", state, startLine, endLine, silent)

    if not state.is_code_block(startLine):
        return False

    last = nextLine = startLine + 1

    while nextLine < endLine:
        if state.isEmpty(nextLine):
            nextLine += 1
            continue

        if state.is_code_block(nextLine):
            nextLine += 1
            last = nextLine
            continue

        break

    state.line = last

    token = state.push("code_block", "code", 0)
    token.content = state.getLines(startLine, last, 4 + state.blkIndent, False) + "\n"
    token.map = [startLine, state.line]

    return True

