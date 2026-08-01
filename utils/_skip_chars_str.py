
def _skipCharsStr(state: StateBlock, pos: int, ch: str) -> int:
    """Skip character string from given position."""
    # TODO this can be replaced with StateBlock.skipCharsStr in markdown-it-py 3.0.0
    while True:
        try:
            current = state.src[pos]
        except IndexError:
            break
        if current != ch:
            break
        pos += 1
    return pos

