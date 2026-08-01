
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi_schema()

    # Filter routes to include only specific ones
    openai_routes = LiteLLMRoutes.openai_routes.value
    paths_to_include: dict = {}
    for route in openai_routes:
        if route in openapi_schema["paths"]:
            paths_to_include[route] = openapi_schema["paths"][route]
    openapi_schema["paths"] = paths_to_include

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

