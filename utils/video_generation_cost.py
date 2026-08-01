
def video_generation_cost(
    model: str,
    duration_seconds: float,
    custom_llm_provider: Optional[str] = None,
    model_info: Optional[ModelInfo] = None,
    video_resolution: Optional[str] = None,
) -> float:
    """
    Calculates the cost for video generation based on duration in seconds.

    Input:
        - model: str, the model name without provider prefix
        - duration_seconds: float, the duration of the generated video in seconds
        - custom_llm_provider: str, the custom llm provider
        - model_info: Optional[dict], deployment-level model info containing
            custom video pricing. When provided, skips the global
            get_model_info() lookup so that deployment-specific pricing is used.
        - video_resolution: Optional resolution label from usage (e.g. ``720p``, ``1080p``).

    Returns:
        float - total_cost_in_usd
    """
    ## GET MODEL INFO
    if model_info is None:
        model_info = get_model_info(
            model=model, custom_llm_provider=custom_llm_provider or "openai"
        )

    # Check for video-specific cost per second
    video_cost_per_second = model_info.get("output_cost_per_video_per_second")
    if video_cost_per_second is not None:
        verbose_logger.debug(
            f"For model={model} - output_cost_per_video_per_second: {video_cost_per_second}; duration: {duration_seconds}"
        )
        return video_cost_per_second * duration_seconds

    output_cost_per_second = _video_output_cost_per_second(model_info, video_resolution)
    if output_cost_per_second is not None:
        verbose_logger.debug(
            f"For model={model} - output_cost_per_second: {output_cost_per_second}; duration: {duration_seconds}"
        )
        return output_cost_per_second * duration_seconds

    # If no cost information found, return 0
    verbose_logger.warning(
        f"No cost information found for video model {model}. Please add pricing to model_prices_and_context_window.json"
    )
    return 0.0

