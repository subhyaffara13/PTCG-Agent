import re

def _word_boundary_match(text: str, token: str) -> bool:
    """True if token appears as a word in text."""
    return bool(re.search(r"\b" + re.escape(token) + r"\b", text))

