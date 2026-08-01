
def _has_meaningful_content(value: Any) -> bool:
    """
    Check if a value contains meaningful content.

    Args:
        value: The value to check

    Returns:
        bool: True if the value has meaningful content, False otherwise
    """
    if value is None:
        return False

    if isinstance(value, str):
        # Don't strip whitespace - preserve all content including newlines, spaces, etc.
        # Even pure whitespace characters like '\n' or ' ' are meaningful content
        return len(value) > 0

    if isinstance(value, (list, dict)):
        return len(value) > 0

    if isinstance(value, bool):
        return True  # Any boolean value is meaningful

    if isinstance(value, (int, float)):
        return True  # Any numeric value is meaningful

    # For other types (objects), consider them meaningful if they exist
    return True

