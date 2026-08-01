
def is_anthropic_native_web_search_tool(tool: Dict[str, Any]) -> bool:
    """
    Check if a tool is an Anthropic-native ``web_search_*`` tool.

    Native clients (Anthropic SDK, Claude Desktop, Anthropic Console) send
    tools like ``{"type": "web_search_20250305", "name": "web_search"}`` and
    expect the response to contain ``web_search_tool_result`` content blocks
    so that citations can be rendered. This helper identifies that contract
    so the agentic loop can emit native-format blocks for those clients
    without affecting clients that send the LiteLLM standard tool.

    Returns False for the LiteLLM standard tool (``litellm_web_search``),
    the OpenAI-shaped variant, the bare ``WebSearch`` legacy name, and the
    bare ``web_search`` name (Claude Code style).
    """
    tool_type = tool.get("type", "")
    if not isinstance(tool_type, str):
        return False
    return tool_type.startswith("web_search_") and tool_type != "function"

