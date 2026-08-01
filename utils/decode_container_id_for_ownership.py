
def decode_container_id_for_ownership(
    container_id: str, custom_llm_provider: str
) -> Tuple[str, str]:
    decoded = ResponsesAPIRequestUtils._decode_container_id(container_id)
    original_container_id = decoded.get("response_id", container_id)
    decoded_provider = decoded.get("custom_llm_provider")
    if decoded_provider and custom_llm_provider == "openai":
        custom_llm_provider = decoded_provider
    return original_container_id, custom_llm_provider

