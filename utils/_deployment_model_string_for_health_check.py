
def _deployment_model_string_for_health_check(litellm_params: dict) -> str:
    """Deployment model from litellm_params (before Bedrock rewrite).

    Used for reasoning vs non-reasoning max_tokens and wildcard detection only.
    Does not use ``health_check_model``; that override applies later to the request.
    """
    return litellm_params.get("model") or ""

