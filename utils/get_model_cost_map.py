import os

def get_model_cost_map(url: str) -> dict:
    """
    Public entry point — returns the model cost map dict.

    1. If ``LITELLM_LOCAL_MODEL_COST_MAP`` is set, uses the local backup only.
    2. Otherwise fetches from ``url``, validates integrity, and falls back
       to the local backup on any failure.

    Only the backup model count is cached (a single int) for validation.
    The full backup dict is only parsed when it must be *returned* as a
    fallback — it is never held in memory long-term.
    """
    # Note: can't use get_secret_bool here — this runs during litellm.__init__
    # before litellm._key_management_settings is set.
    if os.getenv("LITELLM_LOCAL_MODEL_COST_MAP", "").lower() == "true":
        _cost_map_source_info.source = "local"
        _cost_map_source_info.url = None
        _cost_map_source_info.is_env_forced = True
        _cost_map_source_info.fallback_reason = None
        return _expand_model_aliases(GetModelCostMap.load_local_model_cost_map())

    _cost_map_source_info.url = url
    _cost_map_source_info.is_env_forced = False

    try:
        content = GetModelCostMap.fetch_remote_model_cost_map(url)
    except Exception as e:
        verbose_logger.warning(
            "LiteLLM: Failed to fetch remote model cost map from %s: %s. "
            "Falling back to local backup.",
            url,
            str(e),
        )
        _cost_map_source_info.source = "local"
        _cost_map_source_info.fallback_reason = f"Remote fetch failed: {str(e)}"
        return _expand_model_aliases(GetModelCostMap.load_local_model_cost_map())

    # Validate using cached count (cheap int comparison, no file I/O)
    if not GetModelCostMap.validate_model_cost_map(
        fetched_map=content,
        backup_model_count=GetModelCostMap._get_backup_model_count(),
    ):
        verbose_logger.warning(
            "LiteLLM: Fetched model cost map failed integrity check. "
            "Using local backup instead. url=%s",
            url,
        )
        _cost_map_source_info.source = "local"
        _cost_map_source_info.fallback_reason = (
            "Remote data failed integrity validation"
        )
        return _expand_model_aliases(GetModelCostMap.load_local_model_cost_map())

    _cost_map_source_info.source = "remote"
    _cost_map_source_info.fallback_reason = None
    return _expand_model_aliases(content)

