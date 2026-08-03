import re

def amsmath_block(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    # note the code principally follows the logic in markdown_it/rules_block/fence.py,
    # except that:
    # (a) it allows for closing tag on same line as opening tag
    # (b) it does not allow for opening tag without closing tag (i.e. no auto-closing)

    if is_code_block(state, startLine):
        return False

    # does the first line contain the beginning of an amsmath environment
    first_start = state.bMarks[startLine] + state.tShift[startLine]
    first_end = state.eMarks[startLine]
    first_text = state.src[first_start:first_end]

    if not (match_open := re.match(RE_OPEN, first_text)):
        return False

    # construct the closing tag
    environment = match_open.group(1)
    numbered = match_open.group(2)
    closing = rf"\end{{{match_open.group(1)}{match_open.group(2)}}}"

    # start looking for the closing tag, including the current line
    nextLine = startLine - 1

    while True:
        nextLine += 1
        if nextLine >= endLine:
            # reached the end of the block without finding the closing tag
            return False

        next_start = state.bMarks[nextLine] + state.tShift[nextLine]
        next_end = state.eMarks[nextLine]
        if next_start < first_end and state.sCount[nextLine] < state.blkIndent:
            # non-empty line with negative indent should stop the list:
            # - \begin{align}
            #  test
            return False

        if state.src[next_start:next_end].rstrip().endswith(closing):
            # found the closing tag
            break

    state.line = nextLine + 1

    if not silent:
        token = state.push("amsmath", "math", 0)
        token.block = True
        token.content = state.getLines(
            startLine, state.line, state.sCount[startLine], False
        )
        token.meta = {"environment": environment, "numbered": numbered}
        token.map = [startLine, nextLine]

    return True

