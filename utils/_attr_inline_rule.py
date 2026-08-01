
def _attr_inline_rule(
    state: StateInline,
    silent: bool,
    after: Sequence[str],
    *,
    allowed: set[str] | None = None,
) -> bool:
    if state.pending or not state.tokens:
        return False
    token = state.tokens[-1]
    if token.type not in after:
        return False
    try:
        new_pos, attrs = parse(state.src[state.pos :])
    except ParseError:
        return False
    token_index = _find_opening(state.tokens, len(state.tokens) - 1)
    if token_index is None:
        return False
    state.pos += new_pos + 1
    if not silent:
        attr_token = state.tokens[token_index]
        if "class" in attrs and "class" in token.attrs:
            attrs["class"] = f"{token.attrs['class']} {attrs['class']}"
        _add_attrs(attr_token, attrs, allowed)
    return True

