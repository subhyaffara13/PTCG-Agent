
def _build_model_param_to_info_mapping(model_list: list) -> dict:
    """
    Build a mapping from model parameter to model info (model_name, model_id).

    Multiple models might share the same model parameter, so we use a list.

    Args:
        model_list: List of model configurations

    Returns:
        Dictionary mapping model parameter to list of model info dicts
    """
    model_param_to_info: dict = {}
    for model in model_list:
        model_info = model.get("model_info", {})
        model_name = model.get("model_name")
        model_id = model_info.get("id")
        litellm_params = model.get("litellm_params", {})
        model_param = litellm_params.get("model")

        if model_param and model_name:
            if model_param not in model_param_to_info:
                model_param_to_info[model_param] = []
            model_param_to_info[model_param].append(
                {
                    "model_name": model_name,
                    "model_id": model_id,
                }
            )
    return model_param_to_info

