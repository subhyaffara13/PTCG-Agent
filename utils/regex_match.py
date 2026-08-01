
def regex_match(text: str, pattern: str, flags: int = 0) -> bool:
    """
    Check if a regex pattern matches anywhere in the text.

    Args:
        text: The text to search in
        pattern: The regex pattern to match
        flags: Optional regex flags (default: 0)

    Returns:
        True if pattern matches, False otherwise
    """
    try:
        return bool(re.search(pattern, text, flags))
    except re.error as e:
        verbose_proxy_logger.warning(f"Starlark regex_match error: {e}")
        return False

