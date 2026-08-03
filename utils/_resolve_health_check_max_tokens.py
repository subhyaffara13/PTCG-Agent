from typing import Optional

def _resolve_health_check_max_tokens(
    model_info: dict, litellm_params: dict
) -> Optional[int]:
    """
    Pick max_tokens for the health check request.

    Priority:
    1. model_info.health_check_max_tokens (explicit override)
    2. For non-wildcard routes: health_check_max_tokens_reasoning / _non_reasoning
       from model_info based on litellm.supports_reasoning(litellm_params["model"])
    3. For non-wildcard reasoning routes: BACKGROUND_HEALTH_CHECK_MAX_TOKENS_REASONING
       from env (if set)
    4. BACKGROUND_HEALTH_CHECK_MAX_TOKENS (global, any route including wildcards)
    5. Non-wildcard default: 16
    6. Wildcard and nothing from (1)(4): leave unset (caller omits max_tokens)
    """
    explicit = model_info.get("health_check_max_tokens", None)
    if explicit is not None:
        return int(explicit)

    is_wildcard = _health_check_deployment_is_wildcard(litellm_params)
    deployment_model = _deployment_model_string_for_health_check(litellm_params)

    if not is_wildcard:
        try:
            is_reasoning = litellm.supports_reasoning(deployment_model)
        except Exception:
            is_reasoning = False
        tokens_reasoning = model_info.get("health_check_max_tokens_reasoning", None)
        tokens_non_reasoning = model_info.get(
            "health_check_max_tokens_non_reasoning", None
        )
        if tokens_reasoning is not None or tokens_non_reasoning is not None:
            if is_reasoning and tokens_reasoning is not None:
                return int(tokens_reasoning)
            if not is_reasoning and tokens_non_reasoning is not None:
                return int(tokens_non_reasoning)
        if is_reasoning and BACKGROUND_HEALTH_CHECK_MAX_TOKENS_REASONING is not None:
            return int(BACKGROUND_HEALTH_CHECK_MAX_TOKENS_REASONING)

    if BACKGROUND_HEALTH_CHECK_MAX_TOKENS is not None:
        return int(BACKGROUND_HEALTH_CHECK_MAX_TOKENS)

    if not is_wildcard:
        return 16

    return None

