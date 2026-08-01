
def getLine(state: StateBlock, line: int) -> str:
    pos = state.bMarks[line] + state.tShift[line]
    maximum = state.eMarks[line]

    # return state.src.substr(pos, max - pos)
    return state.src[pos:maximum]

