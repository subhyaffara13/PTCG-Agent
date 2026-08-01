
def admonition(state: StateBlock, startLine: int, endLine: int, silent: bool) -> bool:
    if is_code_block(state, startLine):
        return False

    start = state.bMarks[startLine] + state.tShift[startLine]
    maximum = state.eMarks[startLine]

    # Check out the first character quickly, which should filter out most of non-containers
    if state.src[start] not in MARKER_CHARS:
        return False

    # Check out the rest of the marker string
    marker = ""
    marker_len = MAX_MARKER_LEN
    while marker_len > 0:
        marker_pos = start + marker_len
        markup = state.src[start:marker_pos]
        if markup in MARKERS:
            marker = markup
            break
        marker_len -= 1
    else:
        return False

    params = state.src[marker_pos:maximum]

    if not _validate(params):
        return False

    # Since start is found, we can report success here in validation mode
    if silent:
        return True

    old_parent = state.parentType
    old_line_max = state.lineMax
    old_indent = state.blkIndent

    blk_start = marker_pos
    while blk_start < maximum and state.src[blk_start] == " ":
        blk_start += 1

    state.parentType = "admonition"
    # Correct block indentation when extra marker characters are present
    marker_alignment_correction = MARKER_LEN - len(marker)
    state.blkIndent += blk_start - start + marker_alignment_correction

    was_empty = False

    # Search for the end of the block
    next_line = startLine
    while True:
        next_line += 1
        if next_line >= endLine:
            # unclosed block should be autoclosed by end of document.
            # also block seems to be autoclosed by end of parent
            break
        pos = state.bMarks[next_line] + state.tShift[next_line]
        maximum = state.eMarks[next_line]
        is_empty = state.sCount[next_line] < state.blkIndent

        # two consecutive empty lines autoclose the block
        if is_empty and was_empty:
            break
        was_empty = is_empty

        if pos < maximum and state.sCount[next_line] < state.blkIndent:
            # non-empty line with negative indent should stop the block:
            # - !!!
            #  test
            break

    # this will prevent lazy continuations from ever going past our end marker
    state.lineMax = next_line

    tags, title = _get_tag(params)
    tag = tags[0]

    token = state.push("admonition_open", "div", 1)
    token.markup = markup
    token.block = True
    token.attrs = {"class": " ".join(["admonition", *tags, *_extra_classes(markup)])}
    token.meta = {"tag": tag}
    token.content = title
    token.info = params
    token.map = [startLine, next_line]

    if title:
        title_markup = f"{markup} {tag}"
        token = state.push("admonition_title_open", "p", 1)
        token.markup = title_markup
        token.attrs = {"class": "admonition-title"}
        token.map = [startLine, startLine + 1]

        token = state.push("inline", "", 0)
        token.content = title
        token.map = [startLine, startLine + 1]
        token.children = []

        token = state.push("admonition_title_close", "p", -1)

    state.md.block.tokenize(state, startLine + 1, next_line)

    token = state.push("admonition_close", "div", -1)
    token.markup = markup
    token.block = True

    state.parentType = old_parent
    state.lineMax = old_line_max
    state.blkIndent = old_indent
    state.line = next_line

    return True

