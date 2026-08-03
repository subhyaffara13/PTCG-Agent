from typing import Optional

def _resolve_model_from_preferences(
    model_preferences: Optional["ModelPreferences"],
    default_model: Optional[str] = None,
) -> str:
    """
    Resolve an LLM model name from MCP ModelPreferences.
    Strategy:
    1. Check hints for substring matches against known model names.
    2. Fall back to priority-based selection (cost/speed/intelligence).
    3. Fall back to the configured default model.
    Args:
        model_preferences: MCP ModelPreferences with hints and priorities.
        default_model: Fallback model if no hint matches.
    Returns:
        A model string suitable for litellm.acompletion().
    """
    import litellm

    # Build list of available model names from proxy Router or litellm.model_list
    available_model_names: list = []
    try:
        from litellm.proxy.proxy_server import llm_router

        if llm_router is not None:
            available_model_names = llm_router.get_model_names()
    except Exception:
        pass
    if not available_model_names and litellm.model_list:
        for entry in litellm.model_list:
            if isinstance(entry, dict):
                name = entry.get("model_name")
                if name:
                    available_model_names.append(name)
            elif isinstance(entry, str):
                available_model_names.append(entry)
    if model_preferences and model_preferences.hints:
        for hint in model_preferences.hints:
            hint_name = getattr(hint, "name", None)
            if not hint_name:
                continue
            # Try direct match first
            if hint_name in available_model_names:
                verbose_logger.debug(
                    "MCP sampling model resolution: direct hint match '%s'",
                    hint_name,
                )
                return hint_name
            # Try substring match against known models
            for model_name in available_model_names:
                if hint_name.lower() in model_name.lower():
                    verbose_logger.debug(
                        "MCP sampling model resolution: substring hint match "
                        "'%s' -> '%s'",
                        hint_name,
                        model_name,
                    )
                    return model_name
        verbose_logger.debug(
            "MCP sampling model resolution: no hint matched from %s "
            "against %d available models",
            [getattr(h, "name", None) for h in model_preferences.hints],
            len(available_model_names),
        )

    # 2. Priority-based selection (cost/speed/intelligence)
    if (
        model_preferences
        and available_model_names
        and _has_priorities(model_preferences)
    ):
        best = _select_model_by_priority(available_model_names, model_preferences)
        if best is not None:
            verbose_logger.debug(
                "MCP sampling model resolution: priority-based selection chose '%s'",
                best,
            )
            return best

    # 3. Use default model from caller
    if default_model:
        verbose_logger.debug(
            "MCP sampling model resolution: using caller-provided default '%s'",
            default_model,
        )
        return default_model
    # Fall back to first available model
    if available_model_names:
        verbose_logger.debug(
            "MCP sampling model resolution: no default configured, "
            "falling back to first available model '%s'",
            available_model_names[0],
        )
        return available_model_names[0]
    # Last resort - use LiteLLM default or raise error
    default_sampling_model = getattr(litellm, "default_mcp_sampling_model", None)
    if default_sampling_model:
        verbose_logger.debug(
            "MCP sampling model resolution: using litellm.default_mcp_sampling_model='%s'",
            default_sampling_model,
        )
        return default_sampling_model
    raise ValueError(
        "No model could be resolved for MCP sampling. Please configure 'default_mcp_sampling_model' in your LiteLLM configuration."
    )

