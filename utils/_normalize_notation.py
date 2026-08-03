import re

def _normalize_notation(notation: str) -> str:
    """Lowercase + collapse whitespace so model and reference compare equal."""
    return re.sub(r"\s+", " ", notation.strip().lower())

