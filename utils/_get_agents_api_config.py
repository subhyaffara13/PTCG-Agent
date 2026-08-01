
def _get_agents_api_config(custom_llm_provider: str):
    config = get_provider_agents_api_config(custom_llm_provider)
    if config is None:
        raise litellm.BadRequestError(
            message=(
                f"Provider '{custom_llm_provider}' does not have a native "
                "agents API. Use the proxy POST /v1/agents endpoint to store "
                "agents locally."
            ),
            model="",
            llm_provider=custom_llm_provider,
        )
    return config

