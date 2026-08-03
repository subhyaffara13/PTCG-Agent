from typing import List

def get_all_route_types() -> List[str]:
    """Get all async route types for registration in route_llm_request.py"""
    config = _load_endpoints_config()
    return [endpoint["async_name"] for endpoint in config["endpoints"]]

