
def _is_bedrock_tool_block(tool: dict) -> bool:
    """
    Check if a tool is already a BedrockToolBlock.

    BedrockToolBlock has one of: systemTool, toolSpec, or cachePoint.
    This is used to detect tools that are already in Bedrock format
    (e.g., systemTool for Nova grounding) vs OpenAI-style function tools
    that need transformation.

    Args:
        tool: The tool dict to check

    Returns:
        True if the tool is already a BedrockToolBlock, False otherwise

    Examples:
        >>> _is_bedrock_tool_block({"systemTool": {"name": "nova_grounding"}})
        True
        >>> _is_bedrock_tool_block({"type": "function", "function": {...}})
        False
    """
    return isinstance(tool, dict) and (
        "systemTool" in tool or "toolSpec" in tool or "cachePoint" in tool
    )

