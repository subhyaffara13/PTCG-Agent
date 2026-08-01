
def _has_no_execution_intent(text: str) -> bool:
    """True if the text clearly indicates the user does not want code/commands run (e.g. explain, don't run)."""
    if not text:
        return False
    lower = text.lower()
    return any(p in lower for p in _NO_EXECUTION_PHRASES)

