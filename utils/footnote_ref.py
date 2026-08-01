
def footnote_ref(
    state: StateInline, silent: bool, *, always_match: bool = False
) -> bool:
    """Process footnote references ([^...])"""

    maximum = state.posMax
    start = state.pos

    # should be at least 4 chars - "[^x]"
    if start + 3 > maximum:
        return False

    footnote_data = _data_from_env(state.env)

    if not (always_match or footnote_data["refs"]):
        return False
    if state.src[start] != "[":
        return False
    if state.src[start + 1] != "^":
        return False

    pos = start + 2
    while pos < maximum:
        if state.src[pos] in (" ", "\n"):
            return False
        if state.src[pos] == "]":
            break
        pos += 1

    if pos == start + 2:  # no empty footnote labels
        return False
    if pos >= maximum:
        return False
    pos += 1

    label = state.src[start + 2 : pos - 1]
    if ((":" + label) not in footnote_data["refs"]) and not always_match:
        return False

    if not silent:
        if footnote_data["refs"].get(":" + label, -1) < 0:
            footnoteId = len(footnote_data["list"])
            footnote_data["list"][footnoteId] = {"label": label, "count": 0}
            footnote_data["refs"][":" + label] = footnoteId
        else:
            footnoteId = footnote_data["refs"][":" + label]

        footnoteSubId = footnote_data["list"][footnoteId]["count"]
        footnote_data["list"][footnoteId]["count"] += 1

        token = state.push("footnote_ref", "", 0)
        token.meta = {"id": footnoteId, "subId": footnoteSubId, "label": label}

    state.pos = pos
    state.posMax = maximum
    return True

