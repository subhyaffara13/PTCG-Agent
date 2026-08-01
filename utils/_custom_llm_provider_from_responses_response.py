
def _custom_llm_provider_from_responses_response(
    response: Any,
    default: str = "openai",
) -> str:
    hidden_params: Dict[str, Any] = {}
    if isinstance(response, dict):
        hidden_params = response.get("_hidden_params") or {}
    else:
        hidden_params = getattr(response, "_hidden_params", None) or {}

    provider = hidden_params.get("custom_llm_provider")
    if isinstance(provider, str) and provider:
        return provider
    return default

