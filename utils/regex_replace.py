import re

def regex_replace(text: str, pattern: str, replacement: str, flags: int = 0) -> str:
    """
    Replace all occurrences of a pattern in text.

    Args:
        text: The text to modify
        pattern: The regex pattern to find
        replacement: The replacement string
        flags: Optional regex flags

    Returns:
        The text with replacements applied
    """
    try:
        return re.sub(pattern, replacement, text, flags=flags)
    except re.error as e:
        verbose_proxy_logger.warning(f"Starlark regex_replace error: {e}")
        return text

