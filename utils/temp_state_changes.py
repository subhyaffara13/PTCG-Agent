
def temp_state_changes(state: StateBlock, startLine: int) -> Iterator[None]:
    """Allow temporarily changing certain state attributes."""
    oldTShift = state.tShift[startLine]
    oldSCount = state.sCount[startLine]
    oldBlkIndent = state.blkIndent
    oldSrc = state.src
    yield
    state.blkIndent = oldBlkIndent
    state.tShift[startLine] = oldTShift
    state.sCount[startLine] = oldSCount
    state.src = oldSrc

