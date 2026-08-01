
def _calculate_input_cost(
    prompt_tokens_details: PromptTokensDetailsResult,
    model_info: ModelInfo,
    prompt_base_cost: float,
    cache_read_cost: float,
    cache_creation_cost: float,
    cache_creation_cost_above_1hr: float,
    service_tier: Optional[str] = None,
) -> float:
    """
    Calculates the input cost for a given model, prompt tokens, and completion tokens.
    """
    prompt_cost = float(prompt_tokens_details["text_tokens"]) * prompt_base_cost

    ### CACHE READ COST - Now uses tiered pricing
    prompt_cost += float(prompt_tokens_details["cache_hit_tokens"]) * cache_read_cost

    ### AUDIO COST
    if prompt_tokens_details["audio_tokens"]:
        audio_cost_key = _get_service_tier_cost_key(
            "input_cost_per_audio_token", service_tier
        )
        prompt_cost += calculate_cost_component(
            model_info, audio_cost_key, prompt_tokens_details["audio_tokens"]
        )

    ### IMAGE TOKEN COST
    if prompt_tokens_details["image_tokens"]:
        # For image token costs:
        # First check if input_cost_per_image_token is available. If not, default to generic input_cost_per_token.
        image_token_cost_key = "input_cost_per_image_token"
        if model_info.get(image_token_cost_key) is None:
            image_token_cost_key = "input_cost_per_token"
        prompt_cost += calculate_cost_component(
            model_info, image_token_cost_key, prompt_tokens_details["image_tokens"]
        )

    ### CACHE WRITING COST - Now uses tiered pricing
    if (
        prompt_tokens_details["cache_creation_tokens"]
        or prompt_tokens_details["cache_creation_token_details"] is not None
    ):
        prompt_cost += calculate_cache_writing_cost(
            cache_creation_tokens=prompt_tokens_details["cache_creation_tokens"],
            cache_creation_token_details=prompt_tokens_details[
                "cache_creation_token_details"
            ],
            cache_creation_cost_above_1hr=cache_creation_cost_above_1hr,
            cache_creation_cost=cache_creation_cost,
        )

    ### CHARACTER COST
    if prompt_tokens_details["character_count"]:
        prompt_cost += calculate_cost_component(
            model_info,
            "input_cost_per_character",
            prompt_tokens_details["character_count"],
        )

    ### IMAGE COUNT COST
    if prompt_tokens_details["image_count"]:
        prompt_cost += calculate_cost_component(
            model_info, "input_cost_per_image", prompt_tokens_details["image_count"]
        )

    ### VIDEO LENGTH COST
    if prompt_tokens_details["video_length_seconds"]:
        prompt_cost += calculate_cost_component(
            model_info,
            "input_cost_per_video_per_second",
            prompt_tokens_details["video_length_seconds"],
        )

    return prompt_cost

