
def _check_and_merge_model_level_guardrails(
    data: dict, llm_router: Optional[Router]
) -> dict:
    """
    Check if the model has guardrails defined and merge them with existing guardrails in the request data.

    Args:
        data: The request data dict
        llm_router: The LLM router instance to get deployment info from

    Returns:
        Modified data dict with merged guardrails (if any model-level guardrails exist)
    """
    if llm_router is None:
        return data

    # Get the model ID from the data
    metadata = data.get("metadata") or {}
    model_info = metadata.get("model_info") or {}
    model_id = model_info.get("id", None)

    if model_id is None:
        return data

    # Check if the model has guardrails
    deployment = llm_router.get_deployment(model_id=model_id)
    if deployment is None:
        return data

    model_level_guardrails = deployment.litellm_params.get("guardrails")

    if model_level_guardrails is None:
        return data

    # Merge model-level guardrails with existing ones
    return _merge_guardrails_with_existing(data, model_level_guardrails)

