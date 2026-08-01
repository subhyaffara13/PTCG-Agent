
def footnote_inline(state: StateInline, silent: bool) -> bool:
    """Process inline footnotes (^[...])"""

    maximum = state.posMax
    start = state.pos

    if start + 2 >= maximum:
        return False
    if state.src[start] != "^":
        return False
    if state.src[start + 1] != "[":
        return False

    labelStart = start + 2
    labelEnd = parseLinkLabel(state, start + 1)

    # parser failed to find ']', so it's not a valid note
    if labelEnd < 0:
        return False

    # We found the end of the link, and know for a fact it's a valid link
    # so all that's left to do is to call tokenizer.
    #
    if not silent:
        refs = _data_from_env(state.env)["list"]
        footnoteId = len(refs)

        tokens: list[Token] = []
        state.md.inline.parse(
            state.src[labelStart:labelEnd], state.md, state.env, tokens
        )

        token = state.push("footnote_ref", "", 0)
        token.meta = {"id": footnoteId}

        refs[footnoteId] = {"content": state.src[labelStart:labelEnd], "tokens": tokens}

    state.pos = labelEnd + 1
    state.posMax = maximum
    return True

