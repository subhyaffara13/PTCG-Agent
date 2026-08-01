
def _parse_triple(text: str) -> dict[str, int]:
    """Parse a 'Book: x, Hat: y, Basketball: z' fragment into a dict."""
    match = _TRIPLE_RE.search(text)
    if not match:
        return {k: 0 for k in _ITEM_KEYS}
    return {
        "book": int(match.group(1)),
        "hat": int(match.group(2)),
        "basketball": int(match.group(3)),
    }

