
def getNextLine(state: StateBlock, nextLine: int) -> None | str:
    endLine = state.lineMax

    if nextLine >= endLine or state.isEmpty(nextLine):
        # empty line or end of input
        return None

    isContinuation = False

    # this would be a code block normally, but after paragraph
    # it's considered a lazy continuation regardless of what's there
    if state.is_code_block(nextLine):
        isContinuation = True

    # quirk for blockquotes, this line should already be checked by that rule
    if state.sCount[nextLine] < 0:
        isContinuation = True

    if not isContinuation:
        terminatorRules = state.md.block.ruler.getRules("reference")
        oldParentType = state.parentType
        state.parentType = "reference"

        # Some tags can terminate paragraph without empty line.
        terminate = False
        for terminatorRule in terminatorRules:
            if terminatorRule(state, nextLine, endLine, True):
                terminate = True
                break

        state.parentType = oldParentType

        if terminate:
            # terminated by another block
            return None

    pos = state.bMarks[nextLine] + state.tShift[nextLine]
    maximum = state.eMarks[nextLine]

    # max + 1 explicitly includes the newline
    return state.src[pos : maximum + 1]

