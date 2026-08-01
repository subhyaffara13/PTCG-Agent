
def get_provider_agents_api_config(
    custom_llm_provider: Optional[str],
) -> Optional[BaseAgentsAPIConfig]:
    """
    Return a provider-specific BaseAgentsAPIConfig if the provider has a
    native agent-creation API, or None otherwise.
    """
    from litellm.types.utils import LlmProviders

    if custom_llm_provider == LlmProviders.GEMINI.value:
        from litellm.llms.gemini.agents.transformation import GeminiAgentsConfig

        return GeminiAgentsConfig()
    return None

