from typing import List

def contains_all(text: str, substrings: List[str]) -> bool:
    """
    Check if text contains all of the given substrings.

    Args:
        text: The text to search in
        substrings: List of substrings to find

    Returns:
        True if all substrings are found, False otherwise
    """
    return all(s in text for s in substrings)

