
def get_model_cost_map_source_info() -> dict:
    """
    Return metadata about where the current model cost map was loaded from.

    Returns a dict with:
    - source: "local" or "remote"
    - url: the remote URL attempted (or None for local-only)
    - is_env_forced: True if LITELLM_LOCAL_MODEL_COST_MAP=True forced local usage
    - fallback_reason: human-readable reason if remote failed and local was used
    """
    return {
        "source": _cost_map_source_info.source,
        "url": _cost_map_source_info.url,
        "is_env_forced": _cost_map_source_info.is_env_forced,
        "fallback_reason": _cost_map_source_info.fallback_reason,
    }

