
def decode_managed_container_id_for_request(
    container_id: str,
    custom_llm_provider: str,
    litellm_params: GenericLiteLLMParams,
) -> tuple[str, str, GenericLiteLLMParams]:
    """Decode a LiteLLM-managed container ID for upstream API calls.

    Returns:
        (original_container_id, resolved_provider, updated_litellm_params)
    """
    decoded = ResponsesAPIRequestUtils._decode_container_id(container_id)
    original_container_id = decoded.get("response_id", container_id)

    decoded_provider = decoded.get("custom_llm_provider")
    if decoded_provider and custom_llm_provider == "openai":
        custom_llm_provider = decoded_provider

    decoded_model_id = decoded.get("model_id")
    if decoded_model_id and not litellm_params.get("model_id"):
        litellm_params["model_id"] = decoded_model_id

    return original_container_id, custom_llm_provider, litellm_params

