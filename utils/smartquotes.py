
def smartquotes(state: StateCore) -> None:
    if not state.md.options.typographer:
        return

    for token in state.tokens:
        if token.type != "inline" or not QUOTE_RE.search(token.content):
            continue
        if token.children is not None:
            process_inlines(token.children, state)

