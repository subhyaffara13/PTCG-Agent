
def _has_execution_intent(text: str) -> bool:
    """True if the text clearly requests execution (run, execute, read file, run command, etc.)."""
    if not text:
        return False
    lower = text.lower()
    return any(p in lower for p in _EXECUTION_REQUEST_PHRASES)

