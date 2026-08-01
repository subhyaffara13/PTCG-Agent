
def _normalize_language(tag: str) -> str:
    """Normalize language tag (lowercase, resolve aliases)."""
    tag = (tag or "").strip().lower()
    return LANGUAGE_ALIASES.get(tag, tag)

