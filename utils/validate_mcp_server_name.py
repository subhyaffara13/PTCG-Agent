
def validate_mcp_server_name(
    server_name: str, raise_http_exception: bool = False
) -> None:
    """
    Validate that MCP server name does not contain 'MCP_TOOL_PREFIX_SEPARATOR'.

    Args:
        server_name: The server name to validate
        raise_http_exception: If True, raises HTTPException instead of generic Exception

    Raises:
        Exception or HTTPException: If server name contains 'MCP_TOOL_PREFIX_SEPARATOR'
    """
    if server_name and MCP_TOOL_PREFIX_SEPARATOR in server_name:
        error_message = f"Server name cannot contain '{MCP_TOOL_PREFIX_SEPARATOR}'. Use an alternative character instead Found: {server_name}"
        if raise_http_exception:
            from fastapi import HTTPException
            from starlette import status

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail={"error": error_message}
            )
        else:
            raise Exception(error_message)

