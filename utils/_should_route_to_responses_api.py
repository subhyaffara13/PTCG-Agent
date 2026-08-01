
def _should_route_to_responses_api(custom_llm_provider: Optional[str]) -> bool:
    """Return True when the provider should use the Responses API path.

    Set ``litellm.use_chat_completions_url_for_anthropic_messages = True`` to
    opt out and route OpenAI/Azure requests through chat/completions instead.
    """
    if litellm.use_chat_completions_url_for_anthropic_messages:
        return False
    return custom_llm_provider in _RESPONSES_API_PROVIDERS

