
def _fieldlist_rule(
    state: StateBlock, startLine: int, endLine: int, silent: bool
) -> bool:
    # adapted from markdown_it/rules_block/list.py::list_block

    if is_code_block(state, startLine):
        return False

    posAfterName, name_text = parseNameMarker(state, startLine)
    if posAfterName < 0:
        return False

    # For validation mode we can terminate immediately
    if silent:
        return True

    # start field list
    token = state.push("field_list_open", "dl", 1)
    token.attrSet("class", "field-list")
    token.map = listLines = [startLine, 0]

    # iterate list items
    nextLine = startLine

    with set_parent_type(state, "fieldlist"):
        while nextLine < endLine:
            # create name tokens
            token = state.push("fieldlist_name_open", "dt", 1)
            token.map = [startLine, startLine]
            token = state.push("inline", "", 0)
            token.map = [startLine, startLine]
            token.content = name_text
            token.children = []
            token = state.push("fieldlist_name_close", "dt", -1)

            # set indent positions
            pos = posAfterName
            maximum: int = state.eMarks[nextLine]
            first_line_body_indent = (
                state.sCount[nextLine]
                + posAfterName
                - (state.bMarks[startLine] + state.tShift[startLine])
            )

            # find indent to start of body on first line
            while pos < maximum:
                ch = state.src[pos]

                if ch == "\t":
                    first_line_body_indent += (
                        4 - (first_line_body_indent + state.bsCount[nextLine]) % 4
                    )
                elif ch == " ":
                    first_line_body_indent += 1
                else:
                    break

                pos += 1

            contentStart = pos

            # to figure out the indent of the body,
            # we look at all non-empty, indented lines and find the minimum indent
            block_indent: int | None = None
            _line = startLine + 1
            while _line < endLine:
                # if start_of_content < end_of_content, then non-empty line
                if (state.bMarks[_line] + state.tShift[_line]) < state.eMarks[_line]:
                    if state.tShift[_line] <= state.blkIndent:
                        # the line is not indented relative to the field marker,
                        # so it's the end of the field body
                        break
                    block_indent = (
                        state.tShift[_line]
                        if block_indent is None
                        else min(block_indent, state.tShift[_line])
                    )

                _line += 1

            has_first_line = contentStart < maximum
            if block_indent is None:  # no body content
                if not has_first_line:  # noqa: SIM108
                    # no body or first line, so just use default
                    block_indent = 2
                else:
                    # only a first line, so use it's indent
                    block_indent = first_line_body_indent
            else:
                block_indent = min(block_indent, first_line_body_indent)

            # Run subparser on the field body
            token = state.push("fieldlist_body_open", "dd", 1)
            token.map = [startLine, startLine]

            with temp_state_changes(state, startLine):
                diff = 0
                if has_first_line and block_indent < first_line_body_indent:
                    # this is a hack to get the first line to render correctly
                    # we temporarily "shift" it to the left by the difference
                    # between the first line indent and the block indent
                    # and replace the "hole" left with space,
                    # so that src indexes still match
                    diff = first_line_body_indent - block_indent
                    state.src = (
                        state.src[: contentStart - diff]
                        + " " * diff
                        + state.src[contentStart:]
                    )

                state.tShift[startLine] = contentStart - diff - state.bMarks[startLine]
                state.sCount[startLine] = first_line_body_indent - diff
                state.blkIndent = block_indent

                state.md.block.tokenize(state, startLine, endLine)

            state.push("fieldlist_body_close", "dd", -1)

            nextLine = startLine = state.line
            token.map[1] = nextLine

            if nextLine >= endLine:
                break

            contentStart = state.bMarks[startLine]

            # Try to check if list is terminated or continued.
            if state.sCount[nextLine] < state.blkIndent:
                break

            if is_code_block(state, startLine):
                break

            # get next field item
            posAfterName, name_text = parseNameMarker(state, startLine)
            if posAfterName < 0:
                break

        # Finalize list
        token = state.push("field_list_close", "dl", -1)
        listLines[1] = nextLine
        state.line = nextLine

    return True

