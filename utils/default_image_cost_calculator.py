
def default_image_cost_calculator(
    model: str,
    custom_llm_provider: Optional[str] = None,
    quality: Optional[str] = None,
    n: Optional[int] = 1,  # Default to 1 image
    size: Optional[str] = "1024-x-1024",  # OpenAI default
    optional_params: Optional[dict] = None,
) -> float:
    """
    Default image cost calculator for image generation

    Args:
        model (str): Model name
        image_response (ImageResponse): Response from image generation
        quality (Optional[str]): Image quality setting
        n (Optional[int]): Number of images generated
        size (Optional[str]): Image size (e.g. "1024x1024" or "1024-x-1024")

    Returns:
        float: Cost in USD for the image generation

    Raises:
        Exception: If model pricing not found in cost map
    """
    # Standardize size format to use "-x-"
    size_str: str = size or "1024-x-1024"
    size_str = (
        size_str.replace("x", "-x-")
        if "x" in size_str and "-x-" not in size_str
        else size_str
    )

    # Parse dimensions
    height, width = map(int, size_str.split("-x-"))

    # Build model names for cost lookup
    base_model_name = f"{size_str}/{model}"
    model_name_without_custom_llm_provider: Optional[str] = None
    if custom_llm_provider and model.startswith(f"{custom_llm_provider}/"):
        model_name_without_custom_llm_provider = model.replace(
            f"{custom_llm_provider}/", ""
        )
        base_model_name = (
            f"{custom_llm_provider}/{size_str}/{model_name_without_custom_llm_provider}"
        )
    model_name_with_quality = (
        f"{quality}/{base_model_name}" if quality else base_model_name
    )

    # gpt-image-1 models use low, medium, high quality. If user did not specify quality, use medium fot gpt-image-1 model family
    model_name_with_v2_quality = (
        f"{ImageGenerationRequestQuality.HIGH.value}/{base_model_name}"
    )

    verbose_logger.debug(
        f"Looking up cost for models: {model_name_with_quality}, {base_model_name}"
    )

    model_without_provider = f"{size_str}/{model.split('/')[-1]}"
    model_with_quality_without_provider = (
        f"{quality}/{model_without_provider}" if quality else model_without_provider
    )

    # Try model with quality first, fall back to base model name
    cost_info: Optional[dict] = None
    models_to_check: List[Optional[str]] = [
        model_name_with_quality,
        base_model_name,
        model_name_with_v2_quality,
        model_with_quality_without_provider,
        model_without_provider,
        model,
        model_name_without_custom_llm_provider,
    ]
    for _model in models_to_check:
        if _model is not None and _model in litellm.model_cost:
            cost_info = litellm.model_cost[_model]
            break
    if cost_info is None:
        raise Exception(
            f"Model not found in cost map. Tried checking {models_to_check}"
        )

    # Priority 1: Use per-image pricing if available (for gpt-image-1 and similar models)
    if (
        "input_cost_per_image" in cost_info
        and cost_info["input_cost_per_image"] is not None
    ):
        return cost_info["input_cost_per_image"] * n
    # Priority 2: Fall back to per-pixel pricing for backward compatibility
    elif (
        "input_cost_per_pixel" in cost_info
        and cost_info["input_cost_per_pixel"] is not None
    ):
        return cost_info["input_cost_per_pixel"] * height * width * n
    else:
        raise Exception(
            f"No pricing information found for model {model}. Tried checking {models_to_check}"
        )

