
def _filter_v1_model_info_deployments(
    all_models: List[dict],
    allowed_model_names: Optional[Set[str]],
) -> List[dict]:
    if allowed_model_names is None:
        return all_models
    return [
        model
        for model in all_models
        if _deployment_matches_allowed_model_names(model, allowed_model_names)
    ]

