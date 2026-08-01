
def _deployment_supports_web_search(deployment: Dict) -> bool:
    """
    Check if a deployment supports web search.

    Priority:
    1. Check config-level override in model_info.supports_web_search
    2. Default to True (assume supported unless explicitly disabled)

    Note: Ideally we'd fall back to litellm.supports_web_search() but
    model_prices_and_context_window.json doesn't have supports_web_search
    tags on all models yet. TODO: backfill and add fallback.
    """
    model_info = deployment.get("model_info", {})

    if "supports_web_search" in model_info:
        return model_info["supports_web_search"]

    return True

