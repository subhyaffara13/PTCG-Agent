from typing import List

def get_async_endpoint_names() -> List[str]:
    """Get all async endpoint names for router registration."""
    config = _load_endpoints_config()
    return [endpoint["async_name"] for endpoint in config["endpoints"]]

