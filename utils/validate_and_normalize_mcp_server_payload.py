
def validate_and_normalize_mcp_server_payload(payload: Any) -> None:
    """
    Validate and normalize MCP server payload fields (server_name and alias).

    This function:
    1. Validates that server_name and alias don't contain the MCP_TOOL_PREFIX_SEPARATOR
    2. Normalizes alias by replacing spaces with underscores
    3. Sets default alias if not provided (using server_name as base)

    Args:
        payload: The payload object containing server_name and alias fields

    Raises:
        HTTPException: If validation fails
    """
    # Server name validation: disallow '-'
    if hasattr(payload, "server_name") and payload.server_name:
        validate_mcp_server_name(payload.server_name, raise_http_exception=True)

    # Alias validation: disallow '-'
    if hasattr(payload, "alias") and payload.alias:
        validate_mcp_server_name(payload.alias, raise_http_exception=True)

    # Alias normalization and defaulting
    alias = getattr(payload, "alias", None)
    server_name = getattr(payload, "server_name", None)

    if not alias and server_name:
        alias = normalize_server_name(server_name)
    elif alias:
        alias = normalize_server_name(alias)

    # Update the payload with normalized alias
    if hasattr(payload, "alias"):
        payload.alias = alias

