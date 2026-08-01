
def _deduplicate_litellm_router_models(models: List[Dict]) -> List[Dict]:
    """
    Deduplicate models based on their model_info.id field.
    Returns a list of unique models keeping only the first occurrence of each model ID.

    Args:
        models: List of model dictionaries containing model_info

    Returns:
        List of deduplicated model dictionaries
    """
    seen_ids = set()
    unique_models = []
    for model in models:
        model_id = model.get("model_info", {}).get("id", None)
        if model_id is not None and model_id not in seen_ids:
            unique_models.append(model)
            seen_ids.add(model_id)
    return unique_models

