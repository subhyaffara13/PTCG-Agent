
def _mcp_tool_call_metadata(payload: Mapping[str, object]) -> Mapping[str, object]:
    """The MCP gateway's tool-call metadata, which lives under
    ``StandardLoggingPayload.metadata`` (a ``StandardLoggingMetadata`` key), not
    at the payload's top level."""
    metadata = payload.get("metadata")
    if not isinstance(metadata, Mapping):
        return {}
    meta = metadata.get("mcp_tool_call_metadata")
    return meta if isinstance(meta, Mapping) else {}

