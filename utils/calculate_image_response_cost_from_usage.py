
def calculate_image_response_cost_from_usage(
    model: str,
    image_response: ImageResponse,
    custom_llm_provider: str,
) -> Optional[float]:
    """
    Calculate image generation cost from usage metadata when available.

    Returns:
        Optional[float]: total cost from token usage, or None when usage metadata
        is missing/incomplete and caller should fall back to flat per-image pricing.
    """
    usage = image_response.usage
    if usage is None:
        return None

    prompt_tokens = usage.input_tokens
    completion_tokens = usage.output_tokens
    total_tokens = usage.total_tokens

    if prompt_tokens is None or completion_tokens is None or total_tokens is None:
        return None

    # ImageResponse may carry a default zeroed usage object even when provider
    # usage metadata is absent. Treat this as missing usage and fall back.
    if prompt_tokens == 0 and completion_tokens == 0 and total_tokens == 0:
        return None

    input_tokens_details = getattr(usage, "input_tokens_details", None)
    prompt_tokens_details: Optional[PromptTokensDetailsWrapper] = None
    if input_tokens_details is not None:
        prompt_tokens_details = PromptTokensDetailsWrapper(
            text_tokens=getattr(input_tokens_details, "text_tokens", None),
            image_tokens=getattr(input_tokens_details, "image_tokens", None),
            cached_tokens=0,
        )

    output_tokens_details = getattr(usage, "completion_tokens_details", None)
    if output_tokens_details is None:
        output_tokens_details = getattr(usage, "output_tokens_details", None)

    if output_tokens_details is None:
        completion_tokens_details = CompletionTokensDetailsWrapper(
            text_tokens=0,
            image_tokens=completion_tokens,
            reasoning_tokens=0,
            audio_tokens=0,
        )
    else:
        text_tokens = _get_token_detail_value(output_tokens_details, "text_tokens") or 0
        image_tokens = (
            _get_token_detail_value(output_tokens_details, "image_tokens") or 0
        )
        audio_tokens = (
            _get_token_detail_value(output_tokens_details, "audio_tokens") or 0
        )
        reasoning_tokens = (
            _get_token_detail_value(output_tokens_details, "reasoning_tokens") or 0
        )
        known_output_tokens = (
            text_tokens + image_tokens + audio_tokens + reasoning_tokens
        )
        if completion_tokens > known_output_tokens:
            text_tokens += completion_tokens - known_output_tokens

        completion_tokens_details = CompletionTokensDetailsWrapper(
            text_tokens=text_tokens,
            image_tokens=image_tokens,
            reasoning_tokens=reasoning_tokens,
            audio_tokens=audio_tokens,
        )

    normalized_usage = Usage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        prompt_tokens_details=prompt_tokens_details,
        completion_tokens_details=completion_tokens_details,
    )

    prompt_cost, completion_cost = generic_cost_per_token(
        model=model,
        usage=normalized_usage,
        custom_llm_provider=custom_llm_provider,
    )
    return prompt_cost + completion_cost

