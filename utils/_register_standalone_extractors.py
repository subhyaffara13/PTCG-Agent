
def _register_standalone_extractors() -> None:
    if STANDALONE_EXTRACTORS:
        return
    STANDALONE_EXTRACTORS[CallTypes.generate_content.value] = (
        _extract_generate_content_tool_names
    )
    STANDALONE_EXTRACTORS[CallTypes.agenerate_content.value] = (
        _extract_generate_content_tool_names
    )
    STANDALONE_EXTRACTORS[CallTypes.call_mcp_tool.value] = _extract_mcp_tool_names

