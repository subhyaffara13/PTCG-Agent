
def _match_cell_to_legal(
    raw: str, legal_action_strings: Sequence[str],
) -> str | None:
    """Normalize free-form text to canonical 'a7'-style and match a legal."""
    cell = _algebraic_to_cell(raw)
    if cell is None:
        return None
    canonical = _cell_to_algebraic(*cell)
    return canonical if canonical in set(legal_action_strings) else None

