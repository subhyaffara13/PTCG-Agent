
def is_web_search_tool_chat_completion(tool: Dict[str, Any]) -> bool:
    """
    Check if a tool is a web search tool for Chat Completions API (strict check).

    This is a stricter version that ONLY checks for the exact LiteLLM web search tool name.
    Use this for Chat Completions API to avoid false positives with user-defined tools.

    Detects ONLY:
    - LiteLLM standard: name == "litellm_web_search" (Anthropic format)
    - OpenAI format: type == "function" with function.name == "litellm_web_search"

    Args:
        tool: Tool dictionary to check

    Returns:
        True if tool is exactly the LiteLLM web search tool

    Example:
        >>> is_web_search_tool_chat_completion({"name": "litellm_web_search"})
        True
        >>> is_web_search_tool_chat_completion({"type": "function", "function": {"name": "litellm_web_search"}})
        True
        >>> is_web_search_tool_chat_completion({"name": "web_search"})
        False
        >>> is_web_search_tool_chat_completion({"name": "WebSearch"})
        False
    """
    tool_name = tool.get("name", "")
    tool_type = tool.get("type", "")

    # Check for OpenAI format: {"type": "function", "function": {"name": "litellm_web_search"}}
    if tool_type == "function" and "function" in tool:
        function_def = tool.get("function", {})
        function_name = function_def.get("name", "")
        if function_name == LITELLM_WEB_SEARCH_TOOL_NAME:
            return True

    # Check for LiteLLM standard tool (Anthropic format)
    if tool_name == LITELLM_WEB_SEARCH_TOOL_NAME:
        return True

    return False

