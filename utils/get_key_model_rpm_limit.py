
def get_key_model_rpm_limit(
    user_api_key_dict: UserAPIKeyAuth,
    model_name: Optional[str] = None,
) -> Optional[Dict[str, int]]:
    """
    Get the model rpm limit for a given api key.

    Priority order (returns first found):
    1. Key metadata (model_rpm_limit)
    2. Key model_max_budget (rpm_limit per model)
    3. Team metadata (model_rpm_limit)
    4. Deployment default_api_key_rpm_limit (when model_name is provided)
    """
    # 1. Check key metadata first (takes priority)
    if user_api_key_dict.metadata:
        result = user_api_key_dict.metadata.get("model_rpm_limit")
        if result:
            return result

    # 2. Check model_max_budget
    if user_api_key_dict.model_max_budget:
        model_rpm_limit: Dict[str, Any] = {}
        for model, budget in user_api_key_dict.model_max_budget.items():
            if isinstance(budget, dict) and budget.get("rpm_limit") is not None:
                model_rpm_limit[model] = budget["rpm_limit"]
        if model_rpm_limit:
            return model_rpm_limit

    # 3. Fallback to team metadata
    if user_api_key_dict.team_metadata:
        team_limit = user_api_key_dict.team_metadata.get("model_rpm_limit")
        if team_limit is not None:
            return team_limit

    # 4. Fallback to deployment default_api_key_rpm_limit
    if model_name is not None:
        default_limit = _get_deployment_default_rpm_limit(model_name)
        if default_limit is not None:
            return {model_name: default_limit}

    return None

