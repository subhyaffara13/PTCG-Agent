
def _is_gemini_model(model: Optional[str], custom_llm_provider: Optional[str]) -> bool:
    """
    Check if the target model is a Gemini or Vertex AI Gemini model.
    """
    if custom_llm_provider in ["gemini", "vertex_ai", "vertex_ai_beta"]:
        # For vertex_ai, check if it's actually a Gemini model
        if custom_llm_provider in ["vertex_ai", "vertex_ai_beta"]:
            return model is not None and "gemini" in model.lower()
        return True

    # Check if model name contains gemini
    return model is not None and "gemini" in model.lower()

