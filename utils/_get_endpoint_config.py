
def _get_endpoint_config(endpoint_name: str) -> Optional[Dict]:
    """Get config for a specific endpoint by name."""
    config = _load_endpoints_config()
    for endpoint in config["endpoints"]:
        if endpoint["name"] == endpoint_name or endpoint["async_name"] == endpoint_name:
            return endpoint
    return None

