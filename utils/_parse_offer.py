
def _parse_offer(text: str) -> dict[str, int] | None:
    """Parse an 'Offer: Book: x, Hat: y, Basketball: z' line into items."""
    match = _OFFER_RE.search(text)
    if not match:
        return None
    return {
        "book": int(match.group(1)),
        "hat": int(match.group(2)),
        "basketball": int(match.group(3)),
    }

