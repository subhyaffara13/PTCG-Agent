
def _health_check_deployment_is_wildcard(litellm_params: dict) -> bool:
    return "*" in _deployment_model_string_for_health_check(litellm_params)

