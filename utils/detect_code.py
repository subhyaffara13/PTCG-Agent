
def detect_code(text: str) -> bool:
    """
    Check if text contains code of any language.

    Args:
        text: The text to check

    Returns:
        True if code is detected, False otherwise
    """
    return len(detect_code_languages(text)) > 0

