
def _strip_action_id_prefix(action_string: str) -> str:
    """``"648 - Bar/21 Bar/20"`` -> ``"Bar/21 Bar/20"``.

    Legal-move strings from OpenSpiel always start with the action id and a
    ``" - "`` separator; the LLM is asked to write only the right-hand side.
    """
    sep = " - "
    idx = action_string.find(sep)
    return action_string[idx + len(sep) :] if idx >= 0 else action_string

