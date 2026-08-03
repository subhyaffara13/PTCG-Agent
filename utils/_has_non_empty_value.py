from typing import Any

def _has_non_empty_value(value: Any) -> bool:
    """Check if a value has real content (not None, not empty list, not blank string)."""
    if value is None:
        return False
    if isinstance(value, list) and len(value) == 0:
        return False
    if isinstance(value, str) and value.strip() == "":
        return False
    return True

