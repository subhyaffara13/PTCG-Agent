import re
from typing import List

def regex_find_all(text: str, pattern: str, flags: int = 0) -> List[str]:
    """
    Find all occurrences of a pattern in text.

    Args:
        text: The text to search
        pattern: The regex pattern to find
        flags: Optional regex flags

    Returns:
        List of all matches
    """
    try:
        return re.findall(pattern, text, flags)
    except re.error as e:
        verbose_proxy_logger.warning(f"Starlark regex_find_all error: {e}")
        return []

