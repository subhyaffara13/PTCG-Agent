
def is_mcp_tool_call(payload: Mapping[str, object]) -> bool:
    """Whether a closed request's payload is an MCP tool call rather than an LLM
    call — true when the MCP gateway stamped its tool-call metadata, or the call
    type says so on a path that hasn't populated the metadata yet."""
    return bool(_mcp_tool_call_metadata(payload)) or (
        payload.get("call_type") == "call_mcp_tool"
    )

