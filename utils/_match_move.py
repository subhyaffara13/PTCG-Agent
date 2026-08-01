
def _match_move(raw: str, legal: Sequence[str]) -> str | None:
    """Tolerate the capture/coord separators models naturally write.

    Clobber is a capture game and the engine emits bare ``<from><to>``
    strings, but chess-trained models routinely add ``-`` (``a1-b1``),
    ``->`` (``a1->b1``), or the SAN capture marker ``x`` (``a1xb1``).
    Strip those and the surrounding whitespace before comparing.
    """
    target = _normalize_move(raw)
    if not target:
        return None
    for legal_str in legal:
        if _normalize_move(legal_str) == target:
            return legal_str
    return None

