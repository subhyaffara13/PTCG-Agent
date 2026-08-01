
def regex_match_all(text: str, pattern: str, flags: int = 0) -> bool:
    """
    Check if a regex pattern matches the entire text.

    Args:
        text: The text to match
        pattern: The regex pattern
        flags: Optional regex flags

    Returns:
        True if pattern matches entire text, False otherwise
    """
    try:
        return bool(re.fullmatch(pattern, text, flags))
    except re.error as e:
        verbose_proxy_logger.warning(f"Starlark regex_match_all error: {e}")
        return False

