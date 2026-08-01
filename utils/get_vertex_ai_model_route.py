
def get_vertex_ai_model_route(
    model: str, litellm_params: Optional[dict] = None
) -> VertexAIModelRoute:
    """
    Determine which handler to use for a Vertex AI model based on the model name.

    Args:
        model: The model name (e.g., "llama3-405b", "gemini-pro", "gemma/gemma-3-12b-it", "xai/grok-4.1-fast-non-reasoning")
        litellm_params: Optional litellm parameters dict that may contain base_model for routing

    Returns:
        VertexAIModelRoute: The route enum indicating which handler should be used

    Examples:
        >>> get_vertex_ai_model_route("llama3-405b")
        VertexAIModelRoute.PARTNER_MODELS

        >>> get_vertex_ai_model_route("gemini-pro")
        VertexAIModelRoute.GEMINI

        >>> get_vertex_ai_model_route("gemma/gemma-3-12b-it")
        VertexAIModelRoute.GEMMA

        >>> get_vertex_ai_model_route("xai/grok-4.1-fast-non-reasoning")
        VertexAIModelRoute.MODEL_GARDEN

        >>> get_vertex_ai_model_route("1234567890", {"api_base": "http://10.96.32.8"})
        VertexAIModelRoute.GEMINI  # Numeric endpoints with api_base use HTTP path
    """
    from litellm.llms.vertex_ai.vertex_ai_partner_models.main import (
        VertexAIPartnerModels,
    )

    # Check base_model in litellm_params for gemini override
    if litellm_params and litellm_params.get("base_model") is not None:
        if "gemini" in litellm_params["base_model"]:
            return VertexAIModelRoute.GEMINI

    # Check for agent_engine models (Reasoning Engines)
    if "agent_engine/" in model:
        return VertexAIModelRoute.AGENT_ENGINE

    # Check if numeric endpoint ID with custom api_base (PSC endpoint)
    # Route to GEMINI (HTTP path) to support PSC endpoints properly
    if model.isdigit() and litellm_params and litellm_params.get("api_base"):
        return VertexAIModelRoute.GEMINI

    # Check for partner models (llama, mistral, claude, etc.)
    if VertexAIPartnerModels.is_vertex_partner_model(model=model):
        return VertexAIModelRoute.PARTNER_MODELS

    # Check for BGE models
    if "bge/" in model or "bge" in model.lower():
        return VertexAIModelRoute.BGE

    # Check for gemma models
    if "gemma/" in model:
        return VertexAIModelRoute.GEMMA

    # Check for model garden OpenAI-compatible publisher models.
    # Examples:
    # - openai/gpt-oss-120b-maas
    # - xai/grok-4.1-fast-non-reasoning
    if "openai" in model or model.startswith("xai/"):
        return VertexAIModelRoute.MODEL_GARDEN

    # Check for gemini models
    if "gemini" in model:
        return VertexAIModelRoute.GEMINI

    # Default to non-gemini (legacy vertex models like chat-bison, text-bison, etc.)
    return VertexAIModelRoute.NON_GEMINI

