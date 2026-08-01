
def contains_any(text: str, substrings: List[str]) -> bool:
    """
    Check if text contains any of the given substrings.

    Args:
        text: The text to search in
        substrings: List of substrings to find

    Returns:
        True if any substring is found, False otherwise
    """
    return any(s in text for s in substrings)

