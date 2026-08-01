
def _is_azure_model_router_request(model: str) -> bool:
    """
    Check if the requested model is an Azure Model Router.

    Azure Model Router models follow the pattern:
    - azure_ai/model_router/<deployment-name>
    - azure_ai/model-router
    - model_router/<deployment-name>
    - model-router

    Args:
        model: The requested model name

    Returns:
        bool: True if this is an Azure Model Router request
    """
    model_lower = model.lower()
    return "model-router" in model_lower or "model_router" in model_lower

