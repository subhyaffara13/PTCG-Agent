
def handle_key_type(data: GenerateKeyRequest, data_json: dict) -> dict:
    """
    Handle the key type.
    """
    key_type = data.key_type
    data_json.pop("key_type", None)
    if key_type == LiteLLMKeyType.LLM_API:
        data_json["allowed_routes"] = ["llm_api_routes"]
    elif key_type == LiteLLMKeyType.MANAGEMENT:
        data_json["allowed_routes"] = ["management_routes"]
    elif key_type == LiteLLMKeyType.READ_ONLY:
        data_json["allowed_routes"] = ["info_routes"]
    return data_json

