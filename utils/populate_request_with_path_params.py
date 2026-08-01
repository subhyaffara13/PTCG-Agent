
def populate_request_with_path_params(request_data: dict, request: Request) -> dict:
    """
    Copy FastAPI path params and query params into the request payload so downstream checks
    (e.g. vector store RBAC, organization RBAC) see them the same way as body params.

    Since path_params may not be available during dependency injection,
    we parse the URL path directly for known patterns.

    Args:
        request_data: The request data dictionary to populate
        request: The FastAPI Request object

    Returns:
        dict: Updated request_data with path parameters and query parameters added
    """
    # Add query parameters to request_data (for GET requests, etc.)
    query_params = _safe_get_request_query_params(request)
    if query_params:
        for key, value in query_params.items():
            # Don't overwrite existing values from request body
            request_data.setdefault(key, value)

    # Try to get path_params if available (sometimes populated by FastAPI)
    path_params = getattr(request, "path_params", None)
    if isinstance(path_params, dict) and path_params:
        for key, value in path_params.items():
            if key == "vector_store_id":
                request_data.setdefault("vector_store_id", value)
                existing_ids = request_data.get("vector_store_ids")
                if isinstance(existing_ids, list):
                    if value not in existing_ids:
                        existing_ids.append(value)
                else:
                    request_data["vector_store_ids"] = [value]
                continue
            request_data.setdefault(key, value)
        verbose_proxy_logger.debug(
            f"populate_request_with_path_params: Found path_params, vector_store_ids={request_data.get('vector_store_ids')}"
        )
        return request_data

    # Fallback: parse the URL path directly to extract vector_store_id
    _add_vector_store_id_from_path(request_data=request_data, request=request)

    return request_data

