
def _get_container_provider_config(custom_llm_provider: str):
    """Get the container provider config for the given provider."""
    if custom_llm_provider == "openai":
        from litellm.llms.openai.containers.transformation import OpenAIContainerConfig

        return OpenAIContainerConfig()
    elif custom_llm_provider in ("azure", "azure_text"):
        from litellm.llms.azure.containers.transformation import AzureContainerConfig

        return AzureContainerConfig()
    raise ValueError(f"Container API not supported for provider: {custom_llm_provider}")

