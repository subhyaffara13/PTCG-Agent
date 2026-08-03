from typing import List

def get_all_pattern_names() -> List[str]:
    """
    Get a list of all available prebuilt pattern names.

    Returns:
        List of pattern names
    """
    return list(PREBUILT_PATTERNS.keys())

