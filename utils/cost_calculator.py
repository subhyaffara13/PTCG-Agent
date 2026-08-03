from typing import Any, Optional

def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    fal.ai image generation cost calculator
    """
    _model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider=litellm.LlmProviders.FAL_AI.value,
    )
    output_cost_per_image: float = _model_info.get("output_cost_per_image") or 0.0
    num_images: int = 0
    if isinstance(image_response, ImageResponse):
        if image_response.data:
            num_images = len(image_response.data)
        return output_cost_per_image * num_images
    else:
        raise ValueError(
            f"image_response must be of type ImageResponse got type={type(image_response)}"
        )


def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    Recraft image generation cost calculator
    """
    _model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider=litellm.LlmProviders.RECRAFT.value,
    )
    output_cost_per_image: float = _model_info.get("output_cost_per_image") or 0.0
    num_images: int = 0
    if isinstance(image_response, ImageResponse):
        if image_response.data:
            num_images = len(image_response.data)
        return output_cost_per_image * num_images
    else:
        raise ValueError(
            f"image_response must be of type ImageResponse got type={type(image_response)}"
        )


def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    RunwayML image generation cost calculator.

    RunwayML charges per image generated, not per pixel.
    Pricing is stored in model_prices_and_context_window.json with output_cost_per_image.
    """
    _model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider=litellm.LlmProviders.RUNWAYML.value,
    )
    output_cost_per_image: float = _model_info.get("output_cost_per_image") or 0.0
    num_images: int = 0
    if isinstance(image_response, ImageResponse):
        if image_response.data:
            num_images = len(image_response.data)
        return output_cost_per_image * num_images
    else:
        raise ValueError(
            f"image_response must be of type ImageResponse, got type={type(image_response)}"
        )


def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    Vertex AI image edit cost calculator.

    Mirrors image generation pricing: charge per returned image based on
    model metadata (`output_cost_per_image`).
    """
    model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider="vertex_ai",
    )

    output_cost_per_image: float = model_info.get("output_cost_per_image") or 0.0

    if not isinstance(image_response, ImageResponse):
        raise ValueError(
            f"image_response must be of type ImageResponse got type={type(image_response)}"
        )

    num_images = len(image_response.data or [])
    return output_cost_per_image * num_images


def cost_calculator(
    model: str,
    image_response: ImageResponse,
) -> float:
    """
    Vertex AI Image Generation Cost Calculator
    """
    _model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider="vertex_ai",
    )

    web_search_cost = calculate_image_response_web_search_cost(
        image_response=image_response,
        custom_llm_provider="vertex_ai",
        model_info=_model_info,
    )

    token_based_cost = calculate_image_response_cost_from_usage(
        model=model,
        image_response=image_response,
        custom_llm_provider="vertex_ai",
    )
    if token_based_cost is not None:
        return token_based_cost + web_search_cost

    output_cost_per_image: float = _model_info.get("output_cost_per_image") or 0.0
    num_images: int = len(image_response.data) if image_response.data else 0
    return output_cost_per_image * num_images + web_search_cost


def cost_calculator(
    model: str,
    image_response: ImageResponse,
    custom_llm_provider: Optional[str] = None,
) -> float:
    """
    Calculate cost for OpenAI gpt-image models.

    Uses the same usage format as Responses API, so we reuse the helper
    to transform to chat completion format and use generic_cost_per_token.

    Args:
        model: The model name (e.g., "gpt-image-1", "gpt-image-2")
        image_response: The ImageResponse containing usage data
        custom_llm_provider: Optional provider name

    Returns:
        float: Total cost in USD
    """
    usage = getattr(image_response, "usage", None)

    if usage is None:
        verbose_logger.debug(
            f"No usage data available for {model}, cannot calculate token-based cost"
        )
        return 0.0

    # If usage is already a Usage object with completion_tokens_details set,
    # use it directly (it was already transformed in convert_to_image_response)
    if isinstance(usage, Usage) and usage.completion_tokens_details is not None:
        chat_usage = usage
    else:
        # Transform ImageUsage to Usage using the existing helper
        # ImageUsage has the same format as ResponseAPIUsage
        from litellm.responses.utils import ResponseAPILoggingUtils

        chat_usage = (
            ResponseAPILoggingUtils._transform_response_api_usage_to_chat_usage(usage)
        )

    # Use generic_cost_per_token for cost calculation
    prompt_cost, completion_cost = generic_cost_per_token(
        model=model,
        usage=chat_usage,
        custom_llm_provider=custom_llm_provider or "openai",
    )

    total_cost = prompt_cost + completion_cost

    verbose_logger.debug(
        f"OpenAI gpt-image cost calculation for {model}: "
        f"prompt_cost=${prompt_cost:.6f}, completion_cost=${completion_cost:.6f}, "
        f"total=${total_cost:.6f}"
    )

    return total_cost


def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    Gemini image edit cost calculator.

    Gemini image edits and generations share image response billing behavior:
    use provider token usage when present, otherwise fall back to per-image pricing.
    """
    return image_generation_cost_calculator(
        model=model,
        image_response=image_response,
    )


def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    Google AI Image Generation Cost Calculator
    """
    _model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider="gemini",
    )

    if not isinstance(image_response, ImageResponse):
        raise ValueError(
            f"image_response must be of type ImageResponse got type={type(image_response)}"
        )

    web_search_cost = calculate_image_response_web_search_cost(
        image_response=image_response,
        custom_llm_provider="gemini",
        model_info=_model_info,
    )

    token_based_cost = calculate_image_response_cost_from_usage(
        model=model,
        image_response=image_response,
        custom_llm_provider="gemini",
    )
    if token_based_cost is not None:
        return token_based_cost + web_search_cost

    output_cost_per_image: float = _model_info.get("output_cost_per_image") or 0.0
    num_images: int = len(image_response.data) if image_response.data else 0
    return output_cost_per_image * num_images + web_search_cost


def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    CometAPI image generation cost calculator
    """
    _model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider=litellm.LlmProviders.COMETAPI.value,
    )
    output_cost_per_image: float = _model_info.get("output_cost_per_image") or 0.0
    num_images: int = 0
    if isinstance(image_response, ImageResponse):
        if image_response.data:
            num_images = len(image_response.data)
        return output_cost_per_image * num_images
    else:
        raise ValueError(
            f"image_response must be of type ImageResponse got type={type(image_response)}"
        )


def cost_calculator(
    model: str,
    image_response: ImageResponse,
    size: Optional[str] = None,
    optional_params: Optional[dict] = None,
) -> float:
    """
    Bedrock image generation cost calculator

    Handles both Stability 1 and Stability 3 models
    """
    config_class = BedrockImageGeneration.get_config_class(model=model)
    return config_class.cost_calculator(
        model=model,
        image_response=image_response,
        size=size,
        optional_params=optional_params,
    )


def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    Azure AI image generation cost calculator
    """
    _model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider=litellm.LlmProviders.AZURE_AI.value,
    )

    if isinstance(image_response, ImageResponse):
        token_based_cost = calculate_image_response_cost_from_usage(
            model=model,
            image_response=image_response,
            custom_llm_provider=litellm.LlmProviders.AZURE_AI.value,
        )
        if token_based_cost is not None:
            return token_based_cost

        output_cost_per_image: float = _model_info.get("output_cost_per_image") or 0.0
        num_images: int = 0
        if image_response.data:
            num_images = len(image_response.data)
        return output_cost_per_image * num_images

    raise ValueError(
        f"image_response must be of type ImageResponse got type={type(image_response)}"
    )


def cost_calculator(
    model: str,
    image_response: Any,
) -> float:
    """
    AI/ML flux image generation cost calculator
    """
    _model_info = litellm.get_model_info(
        model=model,
        custom_llm_provider=litellm.LlmProviders.AIML.value,
    )
    output_cost_per_image: float = _model_info.get("output_cost_per_image") or 0.0
    num_images: int = 0
    if isinstance(image_response, ImageResponse):
        if image_response.data:
            num_images = len(image_response.data)
        return output_cost_per_image * num_images
    else:
        raise ValueError(
            f"image_response must be of type ImageResponse got type={type(image_response)}"
        )

