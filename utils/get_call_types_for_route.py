from typing import List, Optional

def get_call_types_for_route(route: str) -> Optional[List[CallTypes]]:
    """
    Get the list of CallTypes for a given API route.

    Supports both exact keys and dynamic patterns (e.g. /a2a/my-agent/message/send
    matches /a2a/{agent_id}/message/send).

    Args:
        route: API route path (e.g., "/chat/completions" or "/a2a/my-pydantic-agent/message/send")

    Returns:
        List of CallTypes for that route, or None if route not found
    """
    exact = API_ROUTE_TO_CALL_TYPES.get(route, None)
    if exact is not None:
        return exact
    for pattern, call_types in API_ROUTE_TO_CALL_TYPES.items():
        if _route_matches_pattern(route, pattern):
            return call_types
    return None

