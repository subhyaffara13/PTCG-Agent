from typing import Optional

def _get_deployment_default_limit(model_name: str, field: str) -> Optional[int]:
    """
    Return the minimum value of `field` across all deployments for model_name,
    or None if no deployment has the field set.

    When multiple deployments share the same model name, taking the minimum is
    the safest choice for load-balanced setups: it ensures no deployment is
    over-consumed regardless of which one actually serves a given request.
    """
    from litellm.proxy.proxy_server import llm_router

    if llm_router is None:
        return None
    deployments = llm_router.get_model_list(model_name=model_name)
    if not deployments:
        return None
    limits = []
    for deployment in deployments:
        raw = deployment.get("litellm_params", {}).get(field)
        if raw is not None:
            try:
                if isinstance(raw, (int, float, str, bytes, bytearray)):
                    limits.append(int(raw))
            except (ValueError, TypeError):
                pass
    return min(limits) if limits else None

