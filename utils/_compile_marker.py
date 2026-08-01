
def _compile_marker(pattern: Optional[str]) -> Optional[Pattern[str]]:
    """Compile optional regex string to a pattern."""
    if not pattern or not pattern.strip():
        return None
    try:
        return re.compile(pattern, re.IGNORECASE)
    except re.error:
        return None

