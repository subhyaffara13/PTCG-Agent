
def calculate_image_response_web_search_cost(
    image_response: ImageResponse,
    custom_llm_provider: str,
    model_info: ModelInfo,
) -> float:
    """
    Cost of Google Search grounding performed during image generation.

    The grounding request count is carried on the image usage object by the
    provider transformers; it is billed with the same per-request accounting
    used for chat completions.
    """
    usage = image_response.usage
    if usage is None:
        return 0.0

    web_search_requests = getattr(usage, "web_search_requests", None)
    if not web_search_requests:
        return 0.0

    from litellm.llms import get_cost_for_web_search_request

    synthetic_usage = Usage(
        prompt_tokens_details=PromptTokensDetailsWrapper(
            web_search_requests=web_search_requests
        )
    )
    return (
        get_cost_for_web_search_request(
            custom_llm_provider=custom_llm_provider,
            usage=synthetic_usage,
            model_info=model_info,
        )
        or 0.0
    )

