
def _format_hand(hand: Sequence[str]) -> str:
    """Group cards by suit, e.g. 'Spades: As 5s 9s | Hearts: 2h Th'."""
    if not hand:
        return "(empty)"
    groups: dict[str, list[str]] = {"s": [], "c": [], "d": [], "h": []}
    for card in _sort_cards(hand):
        groups[card[1]].append(card)
    parts: list[str] = []
    for suit in "scdh":
        if groups[suit]:
            parts.append(f"{_SUIT_NAME[suit]}: " + " ".join(groups[suit]))
    return " | ".join(parts) if parts else "(empty)"

