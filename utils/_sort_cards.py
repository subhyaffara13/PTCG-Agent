
def _sort_cards(cards: Sequence[str]) -> list[str]:
    """Sort cards by suit then rank for stable display."""
    return sorted(
        (c for c in cards if _CARD_RE.fullmatch(c)),
        key=lambda c: (_SUIT_ORDER.get(c[1], 99), _RANK_ORDER.get(c[0], 99)),
    )

