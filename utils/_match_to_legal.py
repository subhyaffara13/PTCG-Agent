
def _match_to_legal(
    raw: str | None,
    legal_action_strings: Sequence[str],
) -> str | None:
    """Match a (possibly messy) move string against the legal action list."""
    if raw is None:
        return None
    normalized = _normalize_move(raw)
    if normalized is None:
        return None
    for legal in legal_action_strings:
        if _normalize_legal(legal) == normalized:
            return legal
    return None

