
def get_vertex_ai_image_edit_config(model: str) -> BaseImageEditConfig:
    """
    Get the appropriate image edit config for a Vertex AI model.

    Routes to the correct transformation class based on the model type:
    - Gemini models use generateContent API (VertexAIGeminiImageEditConfig)
    - Imagen models use predict API (VertexAIImagenImageEditConfig)

    Args:
        model: The model name (e.g., "gemini-2.5-flash", "imagegeneration@006")

    Returns:
        BaseImageEditConfig: The appropriate configuration class
    """
    # Determine the model route
    model_route = get_vertex_ai_model_route(model)

    if model_route == VertexAIModelRoute.GEMINI:
        # Gemini models use generateContent API
        return VertexAIGeminiImageEditConfig()
    else:
        # Default to Imagen for other models (imagegeneration, etc.)
        # This includes NON_GEMINI models like imagegeneration@006
        return VertexAIImagenImageEditConfig()

