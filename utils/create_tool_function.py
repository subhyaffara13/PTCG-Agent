import json
from typing import Any, Dict, Optional

def create_tool_function(
    path: str,
    method: str,
    operation: Dict[str, Any],
    base_url: str,
    headers: Optional[Dict[str, str]] = None,
):
    """Create a tool function for an OpenAPI operation.

    This function creates an async tool function that can be called with
    keyword arguments. Parameter names from the OpenAPI spec are accessed
    directly via **kwargs, avoiding syntax errors from invalid Python identifiers.

    Args:
        path: API endpoint path
        method: HTTP method (get, post, put, delete, patch)
        operation: OpenAPI operation object
        base_url: Base URL for the API
        headers: Optional headers to include in requests (e.g., authentication)

    Returns:
        An async function that accepts **kwargs and makes the HTTP request
    """
    if headers is None:
        headers = {}

    path_params, query_params, body_params = extract_parameters(operation)
    original_method = method.lower()

    async def tool_function(**kwargs: Any) -> str:
        """
        Dynamically generated tool function.

        Accepts keyword arguments where keys are the original OpenAPI parameter names.
        The function safely handles parameter names that aren't valid Python identifiers
        by using **kwargs instead of named parameters.
        """
        effective_headers = _merge_openapi_tool_request_headers(headers)

        # Build URL from base_url and path
        url = base_url + path

        # Replace path parameters using original names from OpenAPI spec
        # Apply path traversal validation and URL encoding
        for param_name in path_params:
            param_value = kwargs.get(param_name, "")
            if param_value:
                try:
                    # Sanitize and encode path parameter to prevent traversal attacks
                    safe_value = _sanitize_path_parameter_value(param_value, param_name)
                except ValueError as exc:
                    return "Invalid path parameter: " + str(exc)
                # Replace {param_name} or {{param_name}} in URL
                url = url.replace("{" + param_name + "}", safe_value)
                url = url.replace("{{" + param_name + "}}", safe_value)

        # Build query params using original parameter names
        params: Dict[str, Any] = {}
        for param_name in query_params:
            param_value = kwargs.get(param_name, "")
            if param_value:
                # Use original parameter name in query string (as expected by API)
                params[param_name] = param_value

        # Build request body
        json_body: Optional[Dict[str, Any]] = None
        if body_params:
            # Try "body" first (most common), then check all body param names
            body_value = kwargs.get("body", {})
            if not body_value:
                for param_name in body_params:
                    body_value = kwargs.get(param_name, {})
                    if body_value:
                        break

            if isinstance(body_value, dict):
                json_body = body_value
            elif body_value:
                # If it's a string, try to parse as JSON
                try:
                    json_body = (
                        json.loads(body_value)
                        if isinstance(body_value, str)
                        else {"data": body_value}
                    )
                except (json.JSONDecodeError, TypeError):
                    json_body = {"data": body_value}

        client = get_async_httpx_client(llm_provider=httpxSpecialProvider.MCP)

        if original_method == "get":
            response = await client.get(url, params=params, headers=effective_headers)
        elif original_method == "post":
            response = await client.post(
                url, params=params, json=json_body, headers=effective_headers
            )
        elif original_method == "put":
            response = await client.put(
                url, params=params, json=json_body, headers=effective_headers
            )
        elif original_method == "delete":
            response = await client.delete(
                url, params=params, headers=effective_headers
            )
        elif original_method == "patch":
            response = await client.patch(
                url, params=params, json=json_body, headers=effective_headers
            )
        else:
            return f"Unsupported HTTP method: {original_method}"

        return response.text

    return tool_function

