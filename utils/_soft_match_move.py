
def _soft_match_move(
    candidate: str,
    legal_moves: Sequence[str],
) -> str | None:
    """Try to match a candidate move string to one of the legal moves.

    Replicates the cleaning and matching logic from GameArena's
    ``chess_soft_parser_v1``, adapted to work without python-chess by
    matching against the OpenSpiel legal-move strings directly.
    """
    if not candidate:
        return None

    candidate = candidate.strip()
    if not candidate:
        return None

    # Strip leading move-number prefix (e.g. "1." or "2...")
    if not candidate.startswith("0-0") and candidate[0].isdigit():
        match = re.search(r"(\d+)(\.{1,3})(.*)", candidate)
        if match is not None:
            _, _, candidate = match.groups()
        else:
            return None

    candidate = candidate.lstrip()

    # Remove noise characters
    for ch in _CHARS_TO_REMOVE:
        candidate = candidate.replace(ch, "")

    # Remove en passant annotation
    candidate = candidate.removesuffix("ep")

    if not candidate:
        return None

    # --- Matching stages ---

    # Stage 1: exact match
    if candidate in legal_moves:
        return candidate

    # Stage 2: match ignoring check/checkmate symbols
    candidate_stripped = candidate.rstrip("+#")
    for legal in legal_moves:
        if candidate_stripped == legal.rstrip("+#"):
            return legal

    # Stage 3: case-insensitive match (SAN is normally case-sensitive,
    # but LLMs sometimes change case)
    candidate_lower = candidate_stripped.lower()
    for legal in legal_moves:
        if candidate_lower == legal.rstrip("+#").lower():
            return legal

    return None

