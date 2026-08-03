from typing import Any

def does_mcp_server_exist(
    mcp_server_records: Iterable[Any], mcp_server_id: str
) -> bool:
    """
    Check if the mcp server with the given id exists in the iterable of mcp servers.

    Defined at module level (outside ``if MCP_AVAILABLE``) so it can be imported
    on Python < 3.10 where the ``mcp`` package is unavailable.
    """
    for mcp_server_record in mcp_server_records:
        if mcp_server_record.server_id == mcp_server_id:
            return True
    return False

