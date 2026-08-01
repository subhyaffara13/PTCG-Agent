
def _get_metadata_variable_name(request: Request) -> str:
    """
    Helper to return what the "metadata" field should be called in the request data

    For all /thread or /assistant endpoints we need to call this "litellm_metadata"

    For ALL other endpoints we call this "metadata"
    """
    # Inline imports — auth_utils/route_checks participate in a proxy import cycle.
    from litellm.proxy.auth.auth_utils import get_request_route  # noqa: PLC0415

    path = get_request_route(request)
    if "thread" in path or "assistant" in path:
        return "litellm_metadata"

    if any(route in path for route in LITELLM_METADATA_ROUTES):
        return "litellm_metadata"

    return "metadata"

