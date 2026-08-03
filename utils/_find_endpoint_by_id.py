from typing import List, Optional

def _find_endpoint_by_id(
    endpoints_data: List,
    endpoint_id: str,
) -> Optional[PassThroughGenericEndpoint]:
    """
    Find an endpoint by ID.

    Args:
        endpoints_data: List of endpoint data (dicts or PassThroughGenericEndpoint objects)
        endpoint_id: ID to search for

    Returns:
        Found endpoint or None if not found
    """
    for endpoint in endpoints_data:
        _endpoint: Optional[PassThroughGenericEndpoint] = None
        if isinstance(endpoint, dict):
            _endpoint = PassThroughGenericEndpoint(**endpoint)
        elif isinstance(endpoint, PassThroughGenericEndpoint):
            _endpoint = endpoint

        # Only compare IDs to IDs
        if _endpoint is not None and _endpoint.id == endpoint_id:
            return _endpoint

    return None

