
def _get_deployment_default_rpm_limit(model_name: str) -> Optional[int]:
    return _get_deployment_default_limit(model_name, "default_api_key_rpm_limit")

