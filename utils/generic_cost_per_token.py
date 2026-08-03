from typing import Optional, Tuple

def generic_cost_per_token(
    model: str,
    usage: Usage,
    custom_llm_provider: str,
    service_tier: Optional[str] = None,
    data_residency: Optional[str] = None,
) -> Tuple[float, float]:
    """
    Calculates the cost per token for a given model, prompt tokens, and completion tokens.

    Handles context caching as well.

    Input:
        - model: str, the model name without provider prefix
        - usage: LiteLLM Usage block, containing anthropic caching information
        - data_residency: optional OpenAI data-residency region (e.g. "eu", "us"),
          used to apply the per-model regional-processing uplift multiplier.

    Returns:
        Tuple[float, float] - prompt_cost_in_usd, completion_cost_in_usd
    """

    ## GET MODEL INFO
    model_info = get_model_info(model=model, custom_llm_provider=custom_llm_provider)

    ## CALCULATE INPUT COST
    ### Cost of processing (non-cache hit + cache hit) + Cost of cache-writing (cache writing)
    prompt_cost = 0.0
    ### PROCESSING COST
    prompt_tokens_details = PromptTokensDetailsResult(
        cache_hit_tokens=0,
        cache_creation_tokens=0,
        cache_creation_token_details=None,
        text_tokens=usage.prompt_tokens,
        audio_tokens=0,
        image_tokens=0,
        character_count=0,
        image_count=0,
        video_length_seconds=0.0,
    )
    if usage.prompt_tokens_details:
        prompt_tokens_details = _parse_prompt_tokens_details(usage)

    ## EDGE CASE - text tokens not set or includes cached tokens (double-counting)
    ## Some providers (like xAI) report text_tokens = prompt_tokens (including cached)
    ## We detect this when: text_tokens + cached_tokens + other > prompt_tokens
    ## Ref: https://github.com/BerriAI/litellm/issues/19680, #14874, #14875

    cache_hit = prompt_tokens_details["cache_hit_tokens"]
    text_tokens = prompt_tokens_details["text_tokens"]
    audio_tokens = prompt_tokens_details["audio_tokens"]
    cache_creation = prompt_tokens_details["cache_creation_tokens"]
    image_tokens = prompt_tokens_details["image_tokens"]

    # Check for double-counting: sum of details > prompt_tokens means overlap
    total_details = (
        text_tokens + cache_hit + audio_tokens + cache_creation + image_tokens
    )
    has_double_counting = cache_hit > 0 and total_details > usage.prompt_tokens

    if (
        text_tokens == 0 and prompt_tokens_details["image_count"] == 0
    ) or has_double_counting:
        text_tokens = (
            usage.prompt_tokens
            - cache_hit
            - audio_tokens
            - cache_creation
            - image_tokens
        )
        # Clamp to zero: inconsistent streaming usage
        if text_tokens < 0:
            text_tokens = 0
        prompt_tokens_details["text_tokens"] = text_tokens

    (
        prompt_base_cost,
        completion_base_cost,
        cache_creation_cost,
        cache_creation_cost_above_1hr,
        cache_read_cost,
    ) = _get_token_base_cost(
        model_info=model_info, usage=usage, service_tier=service_tier
    )

    prompt_cost = _calculate_input_cost(
        prompt_tokens_details=prompt_tokens_details,
        model_info=model_info,
        prompt_base_cost=prompt_base_cost,
        cache_read_cost=cache_read_cost,
        cache_creation_cost=cache_creation_cost,
        cache_creation_cost_above_1hr=cache_creation_cost_above_1hr,
        service_tier=service_tier,
    )

    ## CALCULATE OUTPUT COST
    text_tokens = 0
    audio_tokens = 0
    reasoning_tokens = 0
    image_tokens = 0
    is_text_tokens_total = False
    if usage.completion_tokens_details is not None:
        completion_tokens_details = _parse_completion_tokens_details(usage)
        audio_tokens = completion_tokens_details["audio_tokens"]
        text_tokens = completion_tokens_details["text_tokens"]
        reasoning_tokens = completion_tokens_details["reasoning_tokens"]
        image_tokens = completion_tokens_details["image_tokens"]

    # Handle text_tokens calculation:
    # 1. If text_tokens is explicitly provided and > 0, use it
    # 2. If there's a breakdown (reasoning/audio/image tokens), calculate text_tokens as the remainder
    # 3. If no breakdown at all, assume all completion_tokens are text_tokens
    has_token_breakdown = image_tokens > 0 or audio_tokens > 0 or reasoning_tokens > 0
    if text_tokens == 0:
        if has_token_breakdown:
            # Calculate text tokens as remainder when we have a breakdown
            # This handles cases like OpenAI's reasoning models where text_tokens isn't provided
            text_tokens = max(
                0,
                usage.completion_tokens
                - reasoning_tokens
                - audio_tokens
                - image_tokens,
            )
        else:
            # No breakdown at all, all tokens are text tokens
            text_tokens = usage.completion_tokens
            is_text_tokens_total = True
    ## TEXT COST
    completion_cost = float(text_tokens) * completion_base_cost

    ## AUDIO COST
    if not is_text_tokens_total and audio_tokens is not None and audio_tokens > 0:
        _output_cost_per_audio_token = _get_cost_per_unit(
            model_info, "output_cost_per_audio_token", None
        )
        _output_cost_per_audio_token = (
            _output_cost_per_audio_token
            if _output_cost_per_audio_token is not None
            else completion_base_cost
        )
        completion_cost += float(audio_tokens) * _output_cost_per_audio_token

    ## REASONING COST
    if not is_text_tokens_total and reasoning_tokens and reasoning_tokens > 0:
        _output_cost_per_reasoning_token = _get_cost_per_unit(
            model_info, "output_cost_per_reasoning_token", None
        )
        _output_cost_per_reasoning_token = (
            _output_cost_per_reasoning_token
            if _output_cost_per_reasoning_token is not None
            else completion_base_cost
        )
        completion_cost += float(reasoning_tokens) * _output_cost_per_reasoning_token

    ## IMAGE COST
    if not is_text_tokens_total and image_tokens and image_tokens > 0:
        _output_cost_per_image_token = _get_cost_per_unit(
            model_info, "output_cost_per_image_token", None
        )
        _output_cost_per_image_token = (
            _output_cost_per_image_token
            if _output_cost_per_image_token is not None
            else completion_base_cost
        )
        completion_cost += float(image_tokens) * _output_cost_per_image_token

    ## REGIONAL DATA-RESIDENCY UPLIFT
    # Applied as a flat multiplier across all token costs for the request
    # when the upstream is a regionalized OpenAI host (eu./us.api.openai.com).
    uplift = _get_regional_uplift_multiplier(model_info, data_residency)
    if uplift != 1.0:
        prompt_cost *= uplift
        completion_cost *= uplift

    return prompt_cost, completion_cost

