from typing import List, Optional

def default_video_cost_calculator(
    model: str,
    duration_seconds: float,
    custom_llm_provider: Optional[str] = None,
    model_info: Optional[ModelInfo] = None,
    video_resolution: Optional[str] = None,
) -> float:
    """
    Default video cost calculator for video generation

    Args:
        model (str): Model name
        duration_seconds (float): Duration of the generated video in seconds
        custom_llm_provider (Optional[str]): Custom LLM provider
        model_info (Optional[ModelInfo]): Deployment-level model info containing
            custom video pricing. When provided, used before falling back to
            the global litellm.model_cost lookup.
        video_resolution (Optional[str]): From usage (e.g. ``720p``, ``1080p``) for tiered per-second pricing.

    Returns:
        float: Cost in USD for the video generation

    Raises:
        Exception: If model pricing not found in cost map
    """
    # Use custom model_info pricing if provided (deployment-specific pricing)
    cost_info: Optional[dict] = None
    if model_info is not None:
        cost_info = dict(model_info)
    else:
        # Build model names for cost lookup
        base_model_name = model
        model_name_without_custom_llm_provider: Optional[str] = None
        if custom_llm_provider and model.startswith(f"{custom_llm_provider}/"):
            model_name_without_custom_llm_provider = model.replace(
                f"{custom_llm_provider}/", ""
            )
            base_model_name = (
                f"{custom_llm_provider}/{model_name_without_custom_llm_provider}"
            )

        verbose_logger.debug(f"Looking up cost for video model: {base_model_name}")

        model_without_provider = model.split("/")[-1]

        # Try model with provider first, fall back to base model name
        models_to_check: List[Optional[str]] = [
            base_model_name,
            model,
            model_without_provider,
            model_name_without_custom_llm_provider,
        ]
        for _model in models_to_check:
            if _model is not None and _model in litellm.model_cost:
                cost_info = litellm.model_cost[_model]
                break

        # If still not found, try with custom_llm_provider prefix
        if cost_info is None and custom_llm_provider:
            prefixed_model = f"{custom_llm_provider}/{model}"
            if prefixed_model in litellm.model_cost:
                cost_info = litellm.model_cost[prefixed_model]

    if cost_info is None:
        raise Exception(f"Model not found in cost map for model={model}")

    # Check for video-specific cost per second first
    video_cost_per_second = cost_info.get("output_cost_per_video_per_second")
    if video_cost_per_second is not None:
        return video_cost_per_second * duration_seconds

    output_cost_per_second = _video_output_cost_per_second(cost_info, video_resolution)
    if output_cost_per_second is not None:
        return output_cost_per_second * duration_seconds

    # If no cost information found, return 0
    verbose_logger.info(
        f"No cost information found for video model {model}. Please add pricing to model_prices_and_context_window.json"
    )
    return 0.0

