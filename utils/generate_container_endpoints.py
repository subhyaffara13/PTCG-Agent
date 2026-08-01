
def generate_container_endpoints() -> Dict[str, Callable]:
    """
    Generate all container endpoint functions from the JSON config.

    Returns a dict mapping function names to their implementations.
    """
    config = _load_endpoints_config()
    endpoints = {}

    for endpoint_config in config["endpoints"]:
        # Create sync function
        sync_func = create_sync_endpoint_function(endpoint_config)
        endpoints[endpoint_config["name"]] = sync_func

        # Create async function
        async_func = create_async_endpoint_function(sync_func, endpoint_config)
        endpoints[endpoint_config["async_name"]] = async_func

    return endpoints

