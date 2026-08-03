from typing import List

def get_all_endpoint_names() -> List[str]:
    """Get all endpoint names (sync and async) from config."""
    config = _load_endpoints_config()
    names = []
    for endpoint in config["endpoints"]:
        names.append(endpoint["name"])
        names.append(endpoint["async_name"])
    return names

