
def _connection_error_message(exc: BaseException) -> str:
    if isinstance(exc, httpx.LocalProtocolError):
        return (
            "Failed to connect to MCP server: a request header is malformed. "
            "Check static headers for leading/trailing spaces or illegal characters."
        )
    if isinstance(exc, (httpx.ConnectError, httpx.ConnectTimeout)):
        return (
            "Failed to connect to MCP server: the server is unreachable. "
            "Check the URL and that the server is running."
        )
    if isinstance(exc, httpx.TimeoutException):
        return "Failed to connect to MCP server: the connection timed out."
    if isinstance(exc, httpx.HTTPStatusError):
        return (
            f"Failed to connect to MCP server: it returned HTTP "
            f"{exc.response.status_code}."
        )
    return "Failed to connect to MCP server. Check proxy logs for details."

