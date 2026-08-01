
def _match_notation_to_legal(
    raw: str, legal_action_strings: Sequence[str],
) -> str | None:
    """Match a notation string against the legal list.

    Case- and whitespace-insensitive. Forgives missing hit ``*`` and missing
    trailing ``Pass`` markers in either direction (model omits them, or model
    adds them where the legal action didn't have them).
    """
    # Build the lookup with canonical forms first, then register tolerance
    # variants without clobbering canonical entries.
    legal_by_notation: dict[str, str] = {}
    for legal in legal_action_strings:
        notation = _normalize_notation(_strip_action_id_prefix(legal))
        legal_by_notation[notation] = legal
    for legal in legal_action_strings:
        notation = _normalize_notation(_strip_action_id_prefix(legal))
        for variant in _tolerance_variants(notation):
            legal_by_notation.setdefault(variant, legal)

    for candidate in _tolerance_variants(_normalize_notation(raw)):
        match = legal_by_notation.get(candidate)
        if match is not None:
            return match
    return None

