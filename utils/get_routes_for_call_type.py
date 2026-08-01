
def get_routes_for_call_type(call_type: CallTypes) -> list:
    """
    Get all routes that use a specific CallType.

    Args:
        call_type: The CallType to search for

    Returns:
        List of routes that use this CallType
    """
    routes = []
    for route, types in API_ROUTE_TO_CALL_TYPES.items():
        if call_type in types:
            routes.append(route)
    return routes

