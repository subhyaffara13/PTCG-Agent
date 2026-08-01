
def filter_web_search_deployments(
    healthy_deployments: Union[List[Dict], Dict],
    request_kwargs: Optional[Dict] = None,
) -> Union[List[Dict], Dict]:
    """
    If the request is websearch, filter out deployments that don't support web search
    """
    if request_kwargs is None:
        return healthy_deployments
    # When a specific deployment was already chosen, it's returned as a dict
    # rather than a list - nothing to filter, just pass through
    if isinstance(healthy_deployments, dict):
        return healthy_deployments

    is_web_search_request = False
    tools = request_kwargs.get("tools") or []
    for tool in tools:
        # These are the two websearch tools for OpenAI / Azure.
        if tool.get("type") == "web_search" or tool.get("type") == "web_search_preview":
            is_web_search_request = True
            break

    if not is_web_search_request:
        return healthy_deployments

    # Filter out deployments that don't support web search
    final_deployments = [
        d for d in healthy_deployments if _deployment_supports_web_search(d)
    ]
    if len(healthy_deployments) > 0 and len(final_deployments) == 0:
        verbose_logger.warning("No deployments support web search for request")
    return final_deployments

