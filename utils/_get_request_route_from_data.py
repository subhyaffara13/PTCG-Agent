from typing import Optional

def _get_request_route_from_data(request_data: dict) -> Optional[str]:
    """Get request route from request_data (metadata or top-level)."""
    route = request_data.get("user_api_key_request_route")
    if route:
        return route
    meta = request_data.get("metadata") or request_data.get("litellm_metadata") or {}
    return meta.get("user_api_key_request_route")

