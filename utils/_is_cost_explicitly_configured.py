
def _is_cost_explicitly_configured(model: str, llm_router: "Router") -> bool:
    """
    Check if any deployment in the model group has cost fields explicitly
    set in its litellm.model_cost entry.

    When Router._create_deployment() registers a model not in the global
    cost map, it creates a sparse entry like {"id": "<hash>"} with no cost
    fields. _get_model_info_helper() then defaults missing costs to 0.
    This function detects that scenario by checking the raw model_cost entry.
    """
    for deployment in llm_router.model_list:
        if deployment.get("model_name") != model:
            continue
        model_id = deployment.get("model_info", {}).get("id")
        if model_id is None:
            continue
        raw_entry = litellm.model_cost.get(model_id, {})
        if "input_cost_per_token" in raw_entry or "output_cost_per_token" in raw_entry:
            return True
    return False

