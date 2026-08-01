
def _get_deployment_order(deployment: Union[Dict, Any]) -> Optional[int]:
    """
    Returns the routing order for a deployment.

    Checks litellm_params first (static config), then model_info (dynamic/team
    models added via API where order lives in model_info, not litellm_params).
    """
    order = deployment.get("litellm_params", {}).get("order")
    if order is None:
        order = deployment.get("model_info", {}).get("order")
    return order

