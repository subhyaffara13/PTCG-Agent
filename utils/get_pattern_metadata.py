from typing import Dict, List

def get_pattern_metadata() -> List[Dict[str, str]]:
    """
    Return pattern metadata for UI display.

    Returns:
        List of dictionaries containing pattern name, display_name, category, and description
    """
    return [
        {
            "name": pattern_data["name"],
            "display_name": pattern_data["display_name"],
            "category": pattern_data["category"],
            "description": pattern_data["description"],
        }
        for pattern_data in _PATTERNS_DATA["patterns"]
    ]

