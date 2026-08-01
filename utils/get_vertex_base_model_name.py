
def get_vertex_base_model_name(model: str) -> str:
    """
    Strip routing prefixes from model name for PSC/endpoint URL construction.

    Patterns like "bge/", "gemma/", "openai/" are used for internal routing but
    should not appear in the actual endpoint URL. Routing prefixes are derived
    from VertexAIModelRoute enum values.

    Args:
        model: The model name with potential prefix (e.g., "bge/123456", "gemma/gemma-3-12b-it")

    Returns:
        str: The model name without routing prefix (e.g., "123456", "gemma-3-12b-it")

    Examples:
        >>> get_vertex_base_model_name("bge/378943383978115072")
        "378943383978115072"

        >>> get_vertex_base_model_name("gemma/gemma-3-12b-it")
        "gemma-3-12b-it"

        >>> get_vertex_base_model_name("xai/grok-4.1-fast-non-reasoning")
        "grok-4.1-fast-non-reasoning"

        >>> get_vertex_base_model_name("1234567890")
        "1234567890"
    """
    # Derive routing prefixes from VertexAIModelRoute enum
    # Map specific routes to their prefixes (some routes like PARTNER_MODELS, GEMINI don't have prefixes)
    for route in VERTEX_AI_MODEL_ROUTES:
        if model.startswith(route):
            return model.replace(route, "", 1)

    return model

