
def get_openapi_schema():
    if app.openapi_schema:
        return app.openapi_schema

    # Use compatibility wrapper for FastAPI 0.120+ schema generation
    from litellm.proxy.common_utils.openapi_schema_compat import (
        get_openapi_schema_with_compat,
    )

    openapi_schema = get_openapi_schema_with_compat(
        get_openapi_func=get_openapi,
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Find all WebSocket routes
    websocket_routes = [
        route for route in app.routes if isinstance(route, APIWebSocketRoute)
    ]

    # Add a synthetic GET stub for each so they render in Swagger UI,
    # without clobbering existing HTTP operations on the same path.
    openapi_schema = _inject_websocket_stubs_into_openapi_schema(
        openapi_schema, websocket_routes
    )

    # Add LLM API request schema bodies for documentation
    from litellm.proxy.common_utils.custom_openapi_spec import CustomOpenAPISpec

    openapi_schema = CustomOpenAPISpec.add_llm_api_request_schema_body(openapi_schema)

    # Stub unloaded lazy features so they appear as Swagger sections.
    from litellm.proxy._lazy_features import inject_lazy_stubs

    openapi_schema = inject_lazy_stubs(openapi_schema)
    openapi_schema = ensure_unique_openapi_operation_ids(openapi_schema)

    # Fix Swagger UI execute path error when server_root_path is set
    if server_root_path:
        openapi_schema["servers"] = [{"url": "/" + server_root_path.strip("/")}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

