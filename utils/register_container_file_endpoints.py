
def register_container_file_endpoints(router: APIRouter) -> None:
    """
    Register ALL container file endpoints from JSON config to the router.

    This single function registers all endpoints defined in endpoints.json,
    eliminating the need for manual endpoint definitions.
    """
    config = _load_endpoints_config()

    for endpoint_config in config["endpoints"]:
        path = endpoint_config["path"]
        method = endpoint_config["method"].lower()
        path_params = endpoint_config.get("path_params", [])
        route_type = endpoint_config["async_name"]
        returns_binary = endpoint_config.get("returns_binary", False)
        is_multipart = endpoint_config.get("is_multipart", False)

        # Create handler with correct signature for path params
        handler = _create_handler_for_path_params(
            path_params, route_type, returns_binary, is_multipart
        )

        # Register routes
        route_method = getattr(router, method)

        # For binary endpoints, don't use ORJSONResponse
        if returns_binary:
            # Register both /v1/... and /... paths without JSON response class
            route_method(
                f"/v1{path}",
                dependencies=[Depends(user_api_key_auth)],
                tags=["containers"],
            )(handler)

            route_method(
                path,
                dependencies=[Depends(user_api_key_auth)],
                tags=["containers"],
            )(handler)
        else:
            # Register both /v1/... and /... paths with JSON response
            route_method(
                f"/v1{path}",
                dependencies=[Depends(user_api_key_auth)],
                response_class=ORJSONResponse,
                tags=["containers"],
            )(handler)

            route_method(
                path,
                dependencies=[Depends(user_api_key_auth)],
                response_class=ORJSONResponse,
                tags=["containers"],
            )(handler)

