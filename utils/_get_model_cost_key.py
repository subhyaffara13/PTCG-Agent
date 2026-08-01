
def _get_model_cost_key(potential_key: str) -> Optional[str]:
    """
    Get the actual key from model_cost, with case-insensitive fallback.

    WARNING: Only O(1) lookup operations are acceptable. O(n) lookups will cause severe
    CPU overhead. This function is called frequently during router operations.

    ALLOWED HELPER FUNCTIONS (conditionally called, O(n) operations are acceptable):
    - _rebuild_model_cost_lowercase_map: Rebuilds the lookup map (only when map is None)
    - _handle_stale_map_entry_rebuild: Rebuilds map when stale entry detected (rare case)

    If you need to add a new helper function with O(n) operations that is conditionally
    called and confirmed not to cause performance issues, add it to the allowed_helpers
    list in: tests/code_coverage_tests/check_get_model_cost_key_performance.py
    """
    global _model_cost_lowercase_map

    # Exact match (O(1))
    if potential_key in litellm.model_cost:
        return potential_key

    # Case-insensitive lookup via map (O(1))
    if _model_cost_lowercase_map is None:
        _model_cost_lowercase_map = _rebuild_model_cost_lowercase_map()

    potential_key_lower = potential_key.lower()
    matched_key = _model_cost_lowercase_map.get(potential_key_lower)

    # Verify key exists (O(1) - handles model_cost.pop() case)
    if matched_key is not None and matched_key in litellm.model_cost:
        return matched_key

    # Rebuild map if stale entry detected (O(n) rebuild, but only when stale entry found)
    if matched_key is not None:
        matched_key = _handle_stale_map_entry_rebuild(potential_key_lower)
        if matched_key is not None:
            return matched_key

    return None

