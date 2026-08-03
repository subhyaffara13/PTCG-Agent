import sys
from typing import Optional

def supports_response_schema(
    model: str, custom_llm_provider: Optional[str] = None
) -> bool:
    """
    Check if the given model + provider supports 'response_schema' as a param.

    Parameters:
    model (str): The model name to be checked.
    custom_llm_provider (str): The provider to be checked.

    Returns:
    bool: True if the model supports response_schema, False otherwise.

    Does not raise error. Defaults to 'False'. Outputs logging.error.
    """
    ## GET LLM PROVIDER ##
    try:
        get_llm_provider = getattr(sys.modules[__name__], "get_llm_provider")
        model, custom_llm_provider, _, _ = get_llm_provider(
            model=model, custom_llm_provider=custom_llm_provider
        )
    except Exception as e:
        verbose_logger.debug(
            f"Model not found or error in checking response schema support. You passed model={model}, custom_llm_provider={custom_llm_provider}. Error: {str(e)}"
        )
        return False

    # providers that globally support response schema
    PROVIDERS_GLOBALLY_SUPPORT_RESPONSE_SCHEMA = [
        litellm.LlmProviders.PREDIBASE,
        litellm.LlmProviders.FIREWORKS_AI,
        litellm.LlmProviders.LM_STUDIO,
        litellm.LlmProviders.NEBIUS,
        litellm.LlmProviders.DATABRICKS,
    ]

    if custom_llm_provider in PROVIDERS_GLOBALLY_SUPPORT_RESPONSE_SCHEMA:
        return True
    return _supports_factory(
        model=model,
        custom_llm_provider=custom_llm_provider,
        key="supports_response_schema",
    )

