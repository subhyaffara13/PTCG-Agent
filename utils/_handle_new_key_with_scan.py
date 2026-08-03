from typing import Optional

def _handle_new_key_with_scan(
    potential_key_lower: str,
) -> Optional[str]:
    """
    Handle new key added to model_cost without invalidating _model_cost_lowercase_map.

    Scans model_cost for case-insensitive match and rebuilds the map if found.

    Returns:
        The matched key if found, None otherwise.
    """
    global _model_cost_lowercase_map
    for key in litellm.model_cost:
        if key.lower() == potential_key_lower:
            _model_cost_lowercase_map = _rebuild_model_cost_lowercase_map()
            return key
    return None

