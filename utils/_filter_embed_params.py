
def _filter_embed_params(optional_params: dict) -> dict:
    """Map and filter optional_params to only include Gemini embedding fields."""
    gemini_params = optional_params.copy()
    if "dimensions" in gemini_params:
        gemini_params["outputDimensionality"] = gemini_params.pop("dimensions")
    if "task_type" in gemini_params:
        gemini_params["taskType"] = gemini_params.pop("task_type")
    return {k: v for k, v in gemini_params.items() if k in _SUPPORTED_EMBED_PARAMS}

