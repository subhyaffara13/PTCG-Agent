
def _attr_block_rule(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    """Find a block of attributes.

    The block must be a single line that begins with a `{`, after three or less spaces,
    and end with a `}` followed by any number if spaces.
    """
    if is_code_block(state, startLine):
        return False

    pos = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    # if it doesn't start with a {, it's not an attribute block
    if state.src[pos] != "{":
        return False

    # find first non-space character from the right
    while maximum > pos and state.src[maximum - 1] in (" ", "\t"):
        maximum -= 1
    # if it doesn't end with a }, it's not an attribute block
    if maximum <= pos:
        return False
    if state.src[maximum - 1] != "}":
        return False

    try:
        _new_pos, attrs = parse(state.src[pos:maximum])
    except ParseError:
        return False

    # if the block was resolved earlier than expected, it's not an attribute block
    # TODO this was not working in some instances, so I disabled it
    # if (maximum - 1) != new_pos:
    #     return False

    if silent:
        return True

    token = state.push("attrs_block", "", 0)
    token.attrs = attrs  # type: ignore[assignment]
    token.map = [startLine, startLine + 1]

    state.line = startLine + 1
    return True

