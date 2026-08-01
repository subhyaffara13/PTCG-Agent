
def _format_discard_pile(pile: Sequence[str]) -> str:
    """Show the discard pile bottom -> top, marking the top (= upcard)."""
    if not pile:
        return "(empty)"
    cards = list(pile)
    top = cards[-1]
    if len(cards) == 1:
        return f"{top}  (top)"
    return " ".join(cards[:-1]) + f"  [top: {top}]"

