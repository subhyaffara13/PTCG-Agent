
def _invalidate_model_cost_lowercase_map() -> None:
    """Invalidate the case-insensitive lookup map for model_cost.

    Call this whenever litellm.model_cost is modified to ensure the map is rebuilt.
    Also clears related LRU caches that depend on model_cost data.
    """
    global _model_cost_lowercase_map, _model_cost_mutation_generation
    _model_cost_lowercase_map = None
    _model_cost_mutation_generation += 1

    # Clear LRU caches that depend on model_cost data
    _cached_get_model_info.cache_clear()
    _cached_get_model_info_helper.cache_clear()

