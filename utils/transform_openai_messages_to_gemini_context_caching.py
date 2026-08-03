from typing import List, Optional

def transform_openai_messages_to_gemini_context_caching(
    model: str,
    messages: List[AllMessageValues],
    custom_llm_provider: Literal["vertex_ai", "vertex_ai_beta", "gemini"],
    cache_key: str,
    vertex_project: Optional[str],
    vertex_location: Optional[str],
) -> CachedContentRequestBody:
    # Extract TTL from cached messages BEFORE system message transformation
    ttl = extract_ttl_from_cached_messages(messages)

    supports_system_message = get_supports_system_message(
        model=model, custom_llm_provider=custom_llm_provider
    )

    transformed_system_messages, new_messages = _transform_system_message(
        supports_system_message=supports_system_message, messages=messages
    )

    transformed_messages = _gemini_convert_messages_with_history(
        messages=new_messages,
        model=model,
        custom_llm_provider=custom_llm_provider,
    )

    model_name = "models/{}".format(model)

    if custom_llm_provider == "vertex_ai" or custom_llm_provider == "vertex_ai_beta":
        model_name = f"projects/{vertex_project}/locations/{vertex_location}/publishers/google/{model_name}"

    data = CachedContentRequestBody(
        contents=transformed_messages,
        model=model_name,
        displayName=cache_key,
    )

    # Add TTL if present and valid
    if ttl:
        data["ttl"] = ttl

    if transformed_system_messages is not None:
        data["system_instruction"] = transformed_system_messages

    return data

