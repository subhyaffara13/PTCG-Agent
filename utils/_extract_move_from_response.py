
def _extract_move_from_response(
    response: str,
    action_tag: str = "Final Answer:",
    additional_tags: Sequence[str] = (":", "is"),
) -> str | None:
    """Extract a move string from the LLM response.

    Finds the last occurrence of ``action_tag`` or any ``additional_tags``
    in the response and extracts the text that follows, stripping noise.

    This is a faithful port of GameArena's ``parse_move_from_response``
    (from ``parsers.py``) followed by the ``RuleBasedMoveParser``.
    """
    if response is None:
        return None

    last_index = -1
    final_split_token = ""
    for split_token in [action_tag, *additional_tags]:
        tmp_index = response.rfind(split_token)
        if tmp_index > last_index:
            last_index = tmp_index
            final_split_token = split_token

    if last_index == -1:
        return None

    suffix = response[last_index + len(final_split_token) :]
    if suffix is None:
        return None

    move_str = (
        suffix.strip(" .")
        .replace("$", "")
        .replace("\\boxed{", "")
        .replace("\\text{", "")
        .replace("\boxed{", "")
        .replace("\text{", "")
        .replace("}", "")
        .replace("*", "")
        .replace(" ", "")
        .replace("`", "")
        .replace("\n", "")
    )
    move_str = _HTML_TAG_RE.sub("", move_str)

    if not move_str:
        return None

    return move_str


def _extract_move_from_response(response: str, action_tag: str = "Final Answer:") -> str | None:
    """Faithful port of ``parse_move_from_response`` from upstream parsers.py."""
    if response is None:
        return None
    idx = response.rfind(action_tag)
    if idx == -1:
        return None
    suffix = response[idx + len(action_tag) :]
    move_str = (
        suffix.strip(" .")
        .replace("$", "")
        .replace("\\boxed{", "")
        .replace("\\text{", "")
        .replace("\boxed{", "")
        .replace("\text{", "")
        .replace("}", "")
        .replace("*", "")
        .replace(" ", "")
        .replace("`", "")
        .replace("\n", "")
    )
    move_str = _HTML_TAG_RE.sub("", move_str)
    if not move_str:
        return None
    return move_str

