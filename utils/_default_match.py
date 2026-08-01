
def _default_match(raw: str, legals: Sequence[str]) -> str | None:
    """Case-insensitive, whitespace-stripped exact match against legals."""
    target = "".join(raw.split()).lower()
    if not target:
        return None
    for legal in legals:
        if "".join(legal.split()).lower() == target:
            return legal
    return None

