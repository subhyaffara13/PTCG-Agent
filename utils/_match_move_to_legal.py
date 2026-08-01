
def _match_move_to_legal(raw: str, legal_action_strings: Sequence[str]) -> str | None:
    """Match ``raw`` to a legal action string, tolerating common drift.

    Models routinely (a) drop the trailing ``*`` capture marker or
    (b) add one to a non-capture. Try the literal normalization first,
    then try toggling the trailing ``*``.
    """
    if not legal_action_strings:
        return None
    legal_set = set(legal_action_strings)
    candidate = _normalize_move(raw)
    if candidate in legal_set:
        return candidate
    # Try adding a trailing '*' (model forgot the capture marker).
    if not candidate.endswith("*") and f"{candidate}*" in legal_set:
        return f"{candidate}*"
    # Try removing a trailing '*' (model added one to a non-capture).
    if candidate.endswith("*") and candidate[:-1] in legal_set:
        return candidate[:-1]
    return None


def _match_move_to_legal(move: str, legal_moves: Sequence[str]) -> str | None:
    if not move:
        return None
    if move in legal_moves:
        return move
    target = _normalize(move)
    for legal in legal_moves:
        if _normalize(legal) == target:
            return legal
    return None


def _match_move_to_legal(move: str, legal_moves: Sequence[str]) -> str | None:
    if not move:
        return None
    if move in legal_moves:
        return move
    # Tolerate the model echoing the OpenSpiel "Player: X Action: ..." wrapper.
    stripped = _strip_prefix(move)
    if stripped in legal_moves:
        return stripped
    target = _normalize(stripped)
    for legal in legal_moves:
        if _normalize(legal) == target:
            return legal
    return None


def _match_move_to_legal(
    move: str,
    legal_moves: Sequence[str],
) -> str | None:
    """Match a move string (e.g. "e5", "PASS") to a legal move string."""
    move_lower = move.lower()

    if move_lower == "pass":
        for legal in legal_moves:
            if legal.upper().endswith("PASS"):
                return legal
        return None

    for legal in legal_moves:
        parts = legal.split()
        if len(parts) == 2 and parts[1].lower() == move_lower:
            return legal

    return None


def _match_move_to_legal(
    move: str,
    legal_moves: Sequence[str],
) -> str | None:
    """Match a move string against the legal-move list, ignoring case/whitespace.

    Also accepts a move whose separator differs from what the engine reports
    (e.g. the model said "b1-c2" but the actual legal move is "b1xc2"
    because c2 holds an opponent piece).
    """
    target = _normalize(move)
    if not target:
        return None

    legal_normalized = {_normalize(legal): legal for legal in legal_moves}
    if target in legal_normalized:
        return legal_normalized[target]

    # Fall back to matching just the from/to coordinates (ignore separator).
    m = _MOVE_RE.fullmatch(target)
    if not m:
        return None
    coords = (m.group(1).lower(), m.group(2), m.group(4).lower(), m.group(5))
    for legal in legal_moves:
        lm = _MOVE_RE.fullmatch(_normalize(legal))
        if lm and (lm.group(1).lower(), lm.group(2), lm.group(4).lower(), lm.group(5)) == coords:
            return legal

    return None


def _match_move_to_legal(
    move: str,
    legal_action_strings: Sequence[str],
) -> str | None:
    """Match the model's move (a bare direction or full ``ant<i>:dir``) to
    one of the supplied legal action strings.
    """
    target = _normalize(move)
    if not target:
        return None
    for legal in legal_action_strings:
        candidates = {_normalize(legal), _normalize(_direction_only(legal))}
        if target in candidates:
            return legal
    return None

