
def footnote_tail(state: StateCore) -> None:
    """Post-processing step, to move footnote tokens to end of the token stream.

    Also removes un-referenced tokens.
    """

    insideRef = False
    refTokens = {}

    if "footnotes" not in state.env:
        return

    current: list[Token] = []
    tok_filter = []
    for tok in state.tokens:
        if tok.type == "footnote_reference_open":
            insideRef = True
            current = []
            currentLabel = tok.meta["label"]
            tok_filter.append(False)
            continue

        if tok.type == "footnote_reference_close":
            insideRef = False
            # prepend ':' to avoid conflict with Object.prototype members
            refTokens[":" + currentLabel] = current
            tok_filter.append(False)
            continue

        if insideRef:
            current.append(tok)

        tok_filter.append(not insideRef)

    state.tokens = [t for t, f in zip(state.tokens, tok_filter, strict=False) if f]

    footnote_data = _data_from_env(state.env)
    if not footnote_data["list"]:
        return

    token = Token("footnote_block_open", "", 1)
    state.tokens.append(token)

    for i, foot_note in footnote_data["list"].items():
        token = Token("footnote_open", "", 1)
        token.meta = {"id": i, "label": foot_note.get("label", None)}
        # TODO propagate line positions of original foot note
        # (but don't store in token.map, because this is used for scroll syncing)
        state.tokens.append(token)

        if "tokens" in foot_note:
            tokens = []

            token = Token("paragraph_open", "p", 1)
            token.block = True
            tokens.append(token)

            token = Token("inline", "", 0)
            token.children = foot_note["tokens"]
            token.content = foot_note["content"]
            tokens.append(token)

            token = Token("paragraph_close", "p", -1)
            token.block = True
            tokens.append(token)

        elif "label" in foot_note:
            tokens = refTokens.get(":" + foot_note["label"], [])

        state.tokens.extend(tokens)
        if state.tokens[len(state.tokens) - 1].type == "paragraph_close":
            lastParagraph: Token | None = state.tokens.pop()
        else:
            lastParagraph = None

        t = (
            foot_note["count"]
            if (("count" in foot_note) and (foot_note["count"] > 0))
            else 1
        )
        j = 0
        while j < t:
            token = Token("footnote_anchor", "", 0)
            token.meta = {"id": i, "subId": j, "label": foot_note.get("label", None)}
            state.tokens.append(token)
            j += 1

        if lastParagraph:
            state.tokens.append(lastParagraph)

        token = Token("footnote_close", "", -1)
        state.tokens.append(token)

    token = Token("footnote_block_close", "", -1)
    state.tokens.append(token)

