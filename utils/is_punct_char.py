
def isPunctChar(ch: str) -> bool:
    """Check if character is a punctuation character."""
    return unicodedata.category(ch).startswith(("P", "S"))

