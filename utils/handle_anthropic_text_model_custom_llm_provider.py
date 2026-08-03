from typing import Optional, Tuple

def handle_anthropic_text_model_custom_llm_provider(
    model: str, custom_llm_provider: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    """
    if user sets model = "anthropic/claude-2" -> use custom_llm_provider = "anthropic_text"

    Args:
        model:
        custom_llm_provider:

    Returns:
        model, custom_llm_provider
    """

    if custom_llm_provider:
        if (
            custom_llm_provider == "anthropic"
            and litellm.AnthropicTextConfig._is_anthropic_text_model(model)
        ):
            return model, "anthropic_text"

    if model and "/" in model:
        _custom_llm_provider, _model = model.split("/", 1)
        if (
            _custom_llm_provider
            and _custom_llm_provider == "anthropic"
            and litellm.AnthropicTextConfig._is_anthropic_text_model(_model)
        ):
            return _model, "anthropic_text"

    return model, custom_llm_provider

