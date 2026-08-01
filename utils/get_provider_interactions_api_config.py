
def get_provider_interactions_api_config(
    provider: str,
    model: Optional[str] = None,
) -> Optional[BaseInteractionsAPIConfig]:
    """
    Get the interactions API config for the given provider.

    Args:
        provider: The LLM provider name
        model: Optional model name

    Returns:
        The provider-specific interactions API config, or None if not supported
    """
    from litellm.types.utils import LlmProviders

    if provider == LlmProviders.GEMINI.value or provider == "gemini":
        from litellm.llms.gemini.interactions.transformation import (
            GoogleAIStudioInteractionsConfig,
        )

        return GoogleAIStudioInteractionsConfig()

    return None

