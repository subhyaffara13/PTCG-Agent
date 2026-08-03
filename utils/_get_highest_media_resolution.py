from typing import Optional

def _get_highest_media_resolution(
    current: Optional[str], new_detail: Optional[str]
) -> Optional[str]:
    """
    Compare two media resolution values and return the highest one.
    Resolution hierarchy: ultra_high > high > medium > low > None
    """
    resolution_priority = {"ultra_high": 4, "high": 3, "medium": 2, "low": 1}
    current_priority = resolution_priority.get(current, 0) if current else 0
    new_priority = resolution_priority.get(new_detail, 0) if new_detail else 0

    if new_priority > current_priority:
        return new_detail
    return current

