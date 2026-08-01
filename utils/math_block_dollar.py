
def math_block_dollar(
    allow_labels: bool = True,
    label_normalizer: Callable[[str], str] | None = None,
    allow_blank_lines: bool = False,
) -> Callable[[StateBlock, int, int, bool], bool]:
    """Generate block dollar rule."""

    def _math_block_dollar(
        state: StateBlock, startLine: int, endLine: int, silent: bool
    ) -> bool:
        # TODO internal backslash escaping

        if is_code_block(state, startLine):
            return False

        haveEndMarker = False
        startPos = state.bMarks[startLine] + state.tShift[startLine]
        end = state.eMarks[startLine]

        if startPos + 2 > end:
            return False

        if state.src[startPos] != "$" or state.src[startPos + 1] != "$":
            return False

        # search for end of block
        nextLine = startLine
        label = None

        # search for end of block on same line
        lineText = state.src[startPos:end]
        if len(lineText.strip()) > 3:
            if lineText.strip().endswith("$$"):
                haveEndMarker = True
                end = end - 2 - (len(lineText) - len(lineText.strip()))
            elif allow_labels:
                # reverse the line and match
                eqnoMatch = DOLLAR_EQNO_REV.match(lineText[::-1])
                if eqnoMatch:
                    haveEndMarker = True
                    label = eqnoMatch.group(1)[::-1]
                    end = end - eqnoMatch.end()

        # search for end of block on subsequent line
        if not haveEndMarker:
            while True:
                nextLine += 1
                if nextLine >= endLine:
                    break

                start = state.bMarks[nextLine] + state.tShift[nextLine]
                end = state.eMarks[nextLine]

                lineText = state.src[start:end]

                if lineText.strip().endswith("$$"):
                    haveEndMarker = True
                    end = end - 2 - (len(lineText) - len(lineText.strip()))
                    break
                if lineText.strip() == "" and not allow_blank_lines:
                    break  # blank lines are not allowed within $$

                # reverse the line and match
                if allow_labels:
                    eqnoMatch = DOLLAR_EQNO_REV.match(lineText[::-1])
                    if eqnoMatch:
                        haveEndMarker = True
                        label = eqnoMatch.group(1)[::-1]
                        end = end - eqnoMatch.end()
                        break

        if not haveEndMarker:
            return False

        state.line = nextLine + (1 if haveEndMarker else 0)

        token = state.push("math_block_label" if label else "math_block", "math", 0)
        token.block = True
        token.content = state.src[startPos + 2 : end]
        token.markup = "$$"
        token.map = [startLine, state.line]
        if label:
            token.info = label if label_normalizer is None else label_normalizer(label)

        return True

    return _math_block_dollar

