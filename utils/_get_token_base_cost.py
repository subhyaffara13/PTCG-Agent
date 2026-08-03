from typing import Optional, Tuple

def _get_token_base_cost(
    model_info: ModelInfo, usage: Usage, service_tier: Optional[str] = None
) -> Tuple[float, float, float, float, float]:
    """
    Return prompt cost, completion cost, and cache costs for a given model and usage.

    If input_tokens > threshold and `input_cost_per_token_above_[x]k_tokens` or `input_cost_per_token_above_[x]_tokens` is set,
    then we use the corresponding threshold cost for all token types.

    Returns:
        Tuple[float, float, float, float] - (prompt_cost, completion_cost, cache_creation_cost, cache_read_cost)
    """
    # Get service tier aware cost keys
    input_cost_key = _get_service_tier_cost_key("input_cost_per_token", service_tier)
    output_cost_key = _get_service_tier_cost_key("output_cost_per_token", service_tier)
    cache_creation_cost_key = _get_service_tier_cost_key(
        "cache_creation_input_token_cost", service_tier
    )
    cache_read_cost_key = _get_service_tier_cost_key(
        "cache_read_input_token_cost", service_tier
    )

    prompt_base_cost = cast(float, _get_cost_per_unit(model_info, input_cost_key))
    completion_base_cost = cast(float, _get_cost_per_unit(model_info, output_cost_key))

    # For image generation models that don't have output_cost_per_token,
    # use output_cost_per_image_token as the base cost (all output tokens are image tokens)
    if completion_base_cost == 0.0 or completion_base_cost is None:
        output_image_cost = _get_cost_per_unit(
            model_info, "output_cost_per_image_token", None
        )
        if output_image_cost is not None:
            completion_base_cost = cast(float, output_image_cost)
    cache_creation_cost = cast(
        float, _get_cost_per_unit(model_info, cache_creation_cost_key)
    )
    cache_creation_cost_above_1hr = cast(
        float,
        _get_cost_per_unit(model_info, "cache_creation_input_token_cost_above_1hr"),
    )
    cache_read_cost = cast(float, _get_cost_per_unit(model_info, cache_read_cost_key))

    ## CHECK IF ABOVE THRESHOLD
    # Optimization: collect threshold keys first to avoid sorting all model_info keys.
    # Most models don't have threshold pricing, so we can return early.
    # Exclude service_tier-specific variants (e.g. input_cost_per_token_above_200k_tokens_priority)
    # so that the threshold detection loop only processes standard keys.  The
    # service_tier-specific above-threshold key is resolved later via _get_service_tier_cost_key.
    threshold_keys = [
        k
        for k in model_info
        if k.startswith("input_cost_per_token_above_")
        and not any(k.endswith(f"_{st.value}") for st in ServiceTier)
    ]
    if not threshold_keys:
        return (
            prompt_base_cost,
            completion_base_cost,
            cache_creation_cost,
            cache_creation_cost_above_1hr,
            cache_read_cost,
        )

    # Only sort the threshold keys (typically 1-2 keys instead of 66+)
    threshold: Optional[float] = None
    for key in sorted(threshold_keys, key=_parse_above_token_threshold, reverse=True):
        value = model_info.get(key)
        if value is not None:
            try:
                # Handle both formats: _above_128k_tokens and _above_128_tokens
                threshold_str = key.split("_above_")[1].split("_tokens")[0]
                threshold = _parse_above_token_threshold(key)
                if usage.prompt_tokens > threshold:
                    # Prefer a service_tier-specific above-threshold key when available,
                    # e.g. input_cost_per_token_priority_above_200k_tokens for Gemini
                    # ON_DEMAND_PRIORITY.  Falls back to the standard key automatically
                    # via _get_cost_per_unit's service_tier fallback logic.
                    tiered_input_key = (
                        _get_service_tier_cost_key(
                            f"input_cost_per_token_above_{threshold_str}_tokens",
                            service_tier,
                        )
                        if service_tier
                        else key
                    )
                    prompt_base_cost = cast(
                        float,
                        _get_cost_per_unit(
                            model_info, tiered_input_key, prompt_base_cost
                        ),
                    )
                    tiered_output_key = (
                        _get_service_tier_cost_key(
                            f"output_cost_per_token_above_{threshold_str}_tokens",
                            service_tier,
                        )
                        if service_tier
                        else f"output_cost_per_token_above_{threshold_str}_tokens"
                    )
                    completion_base_cost = cast(
                        float,
                        _get_cost_per_unit(
                            model_info,
                            tiered_output_key,
                            completion_base_cost,
                        ),
                    )

                    # Apply tiered pricing to cache costs
                    cache_creation_tiered_key = (
                        _get_service_tier_cost_key(
                            f"cache_creation_input_token_cost_above_{threshold_str}_tokens",
                            service_tier,
                        )
                        if service_tier
                        else f"cache_creation_input_token_cost_above_{threshold_str}_tokens"
                    )
                    cache_creation_1hr_tiered_key = (
                        _get_service_tier_cost_key(
                            f"cache_creation_input_token_cost_above_1hr_above_{threshold_str}_tokens",
                            service_tier,
                        )
                        if service_tier
                        else f"cache_creation_input_token_cost_above_1hr_above_{threshold_str}_tokens"
                    )
                    cache_read_tiered_key = (
                        _get_service_tier_cost_key(
                            f"cache_read_input_token_cost_above_{threshold_str}_tokens",
                            service_tier,
                        )
                        if service_tier
                        else f"cache_read_input_token_cost_above_{threshold_str}_tokens"
                    )

                    cache_creation_cost = cast(
                        float,
                        _get_cost_per_unit(
                            model_info,
                            cache_creation_tiered_key,
                            cache_creation_cost,
                        ),
                    )

                    cache_creation_cost_above_1hr = cast(
                        float,
                        _get_cost_per_unit(
                            model_info,
                            cache_creation_1hr_tiered_key,
                            cache_creation_cost_above_1hr,
                        ),
                    )

                    cache_read_cost = cast(
                        float,
                        _get_cost_per_unit(
                            model_info, cache_read_tiered_key, cache_read_cost
                        ),
                    )

                    break
            except (IndexError, ValueError):
                continue
            except Exception:
                continue

    return (
        prompt_base_cost,
        completion_base_cost,
        cache_creation_cost,
        cache_creation_cost_above_1hr,
        cache_read_cost,
    )

