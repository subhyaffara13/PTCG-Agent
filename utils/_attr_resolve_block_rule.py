
def _attr_resolve_block_rule(state: StateCore, *, allowed: set[str] | None) -> None:
    """Find attribute block then move its attributes to the next block."""
    i = 0
    len_tokens = len(state.tokens)
    while i < len_tokens:
        if state.tokens[i].type != "attrs_block":
            i += 1
            continue

        if i + 1 < len_tokens:
            next_token = state.tokens[i + 1]

            # classes are appended
            if "class" in state.tokens[i].attrs and "class" in next_token.attrs:
                state.tokens[i].attrs["class"] = (
                    f"{state.tokens[i].attrs['class']} {next_token.attrs['class']}"
                )

            if next_token.type == "attrs_block":
                # subsequent attribute blocks take precedence, when merging
                for key, value in state.tokens[i].attrs.items():
                    if key == "class" or key not in next_token.attrs:
                        next_token.attrs[key] = value
            else:
                _add_attrs(next_token, state.tokens[i].attrs, allowed)

        state.tokens.pop(i)
        len_tokens -= 1

