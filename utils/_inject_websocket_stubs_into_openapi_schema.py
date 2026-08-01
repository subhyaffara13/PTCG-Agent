
def _inject_websocket_stubs_into_openapi_schema(
    openapi_schema: dict, websocket_routes: list
) -> dict:
    """
    Add a synthetic GET stub for each WebSocket route so it appears in Swagger UI.

    Merges into any existing path entry rather than replacing it — a WebSocket route
    that shares its path with an HTTP route must not erase the HTTP operation. If
    a "get" operation is already documented on the path, the WebSocket stub is
    skipped to preserve the real GET.
    """
    for route in websocket_routes:
        base_path = route.path.split("{")[0].rstrip("?")

        parameters = []
        try:
            if hasattr(route, "dependant") and route.dependant is not None:
                # Handle both FastAPI <0.120 and >=0.120
                query_params = getattr(route.dependant, "query_params", [])
                if query_params:
                    for param in query_params:
                        parameters.append(
                            {
                                "name": param.name,
                                "in": "query",
                                "required": param.required,
                                "schema": {"type": "string"},
                            }
                        )
        except (AttributeError, TypeError):
            pass

        path_entry = openapi_schema["paths"].setdefault(base_path, {})
        if "get" not in path_entry:
            path_entry["get"] = {
                "summary": f"WebSocket: {route.name or base_path}",
                "description": "WebSocket connection endpoint",
                "operationId": f"websocket_{route.name or base_path.replace('/', '_')}",
                "parameters": parameters,
                "responses": {"101": {"description": "WebSocket Protocol Switched"}},
                "tags": ["WebSocket"],
            }

    return openapi_schema

