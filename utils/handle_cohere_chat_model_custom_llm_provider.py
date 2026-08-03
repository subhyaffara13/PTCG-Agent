from typing import Optional, Tuple

def handle_cohere_chat_model_custom_llm_provider(
    model: str, custom_llm_provider: Optional[str] = None
) -> Tuple[str, Optional[str]]:
    """
    if user sets model = "cohere/command-r" -> use custom_llm_provider = "cohere_chat"

    Args:
        model:
        custom_llm_provider:

    Returns:
        model, custom_llm_provider
    """

    if custom_llm_provider:
        if custom_llm_provider == "cohere" and model in litellm.cohere_chat_models:
            return model, "cohere_chat"

    if model and "/" in model:
        _custom_llm_provider, _model = model.split("/", 1)
        if (
            _custom_llm_provider
            and _custom_llm_provider == "cohere"
            and _model in litellm.cohere_chat_models
        ):
            return _model, "cohere_chat"

    return model, custom_llm_provider

