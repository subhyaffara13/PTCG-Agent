
def _route_requires_auth_despite_public(
    route: str, general_settings: Optional[dict]
) -> bool:
    normalized_route = _normalize_public_auth_route(route)
    if normalized_route == "/metrics":
        return litellm.require_auth_for_metrics_endpoint is not False

    return False

