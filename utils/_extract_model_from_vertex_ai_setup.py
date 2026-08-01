
def _extract_model_from_vertex_ai_setup(setup_response: dict) -> Optional[str]:
    """
    Extract the model name from Vertex AI Live setup response.

    The setup response can contain a model field in two formats:
    1. Direct: {"model": "projects/.../models/gemini-2.0-flash-live-preview-04-09"}
    2. Nested: {"setup": {"model": "projects/.../models/gemini-2.0-flash-live-preview-04-09"}}

    We extract just the model name: "gemini-2.0-flash-live-preview-04-09"
    """
    try:
        # Handle both direct model field and nested setup.model field
        model_path = None
        if isinstance(setup_response, dict):
            if "model" in setup_response:
                model_path = setup_response["model"]
            elif (
                "setup" in setup_response
                and isinstance(setup_response["setup"], dict)
                and "model" in setup_response["setup"]
            ):
                model_path = setup_response["setup"]["model"]

        if isinstance(model_path, str) and "/models/" in model_path:
            # Extract the model name after the last "/models/"
            model_name = model_path.split("/models/")[-1]
            return model_name
    except Exception as e:
        verbose_proxy_logger.debug(f"Error extracting model from setup response: {e}")
    return None

