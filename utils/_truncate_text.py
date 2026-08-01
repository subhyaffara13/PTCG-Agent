
def _truncate_text(text: str, max_chars: int = 30000) -> str:
    """Truncate long text, keeping first and last portions."""
    if len(text) <= max_chars:
        return text
    half = max_chars // 2
    return text[:half] + "\n...\n" + text[-half:]

