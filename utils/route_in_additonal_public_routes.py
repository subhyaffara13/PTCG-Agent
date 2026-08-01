
def route_in_additonal_public_routes(current_route: str):
    """
    Helper to check if the user defined public_routes on config.yaml

    Parameters:
    - current_route: str - the route the user is trying to call

    Returns:
    - bool - True if the route is defined in public_routes
    - bool - False if the route is not defined in public_routes

    Supports wildcard patterns (e.g., "/api/*" matches "/api/users", "/api/users/123")

    In order to use this the litellm config.yaml should have the following in general_settings:

    ```yaml
    general_settings:
        master_key: sk-1234
        public_routes: ["LiteLLMRoutes.public_routes", "/spend/calculate", "/api/*"]
    ```
    """
    from litellm.proxy.auth.route_checks import RouteChecks
    from litellm.proxy.proxy_server import general_settings, premium_user

    try:
        if premium_user is not True:
            return False
        if general_settings is None:
            return False

        routes_defined = general_settings.get("public_routes", [])

        # Check exact match first
        if current_route in routes_defined:
            return True

        # Check wildcard patterns
        for route_pattern in routes_defined:
            if RouteChecks._route_matches_wildcard_pattern(
                route=current_route, pattern=route_pattern
            ):
                return True

        return False
    except Exception as e:
        verbose_proxy_logger.error(f"route_in_additonal_public_routes: {str(e)}")
        return False

