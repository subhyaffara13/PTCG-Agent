
def _handle_stale_map_entry_rebuild(
    potential_key_lower: str,
) -> Optional[str]:
    """
    Handle stale _model_cost_lowercase_map entry (key was popped).

    Rebuilds the map and retries the lookup.

    Returns:
        The matched key if found after rebuild, None otherwise.
    """
    global _model_cost_lowercase_map
    _model_cost_lowercase_map = _rebuild_model_cost_lowercase_map()
    matched_key = _model_cost_lowercase_map.get(potential_key_lower)
    if matched_key is not None and matched_key in litellm.model_cost:
        return matched_key
    return None

