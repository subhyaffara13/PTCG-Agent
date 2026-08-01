
def is_web_search_tool(tool: Dict[str, Any]) -> bool:
    """
    Check if a tool is a web search tool (native or LiteLLM standard).

    Detects:
    - LiteLLM standard: name == "litellm_web_search"
    - OpenAI format: type == "function" with function.name == "litellm_web_search"
    - Anthropic native: type starts with "web_search_" (e.g., "web_search_20250305")
    - Claude Code: name == "web_search" with a type field
    - Custom: name == "WebSearch" (legacy interception marker — only matched
      when input_schema is absent; see note below)

    Note on the legacy ``WebSearch`` name:
        Clients like Claude Desktop / Cowork ship a *client-side* tool called
        ``WebSearch`` (a fully-formed Anthropic client tool with its own
        ``input_schema``) that they handle themselves. Treating that as our
        interception marker hijacks it server-side and the client's own tool
        handler never fires — which means Cowork's separate native
        ``web_search_20250305`` sub-request (where citation data actually
        flows) never gets made.

        Real Anthropic client tools always carry an ``input_schema`` (the API
        rejects them otherwise), so a bare ``{name: "WebSearch"}`` with no
        schema is the only thing that could be a legacy interception marker.
        Gate the match on schema absence to keep both groups working.

    Args:
        tool: Tool dictionary to check

    Returns:
        True if tool is a web search tool

    Example:
        >>> is_web_search_tool({"name": "litellm_web_search"})
        True
        >>> is_web_search_tool({"type": "function", "function": {"name": "litellm_web_search"}})
        True
        >>> is_web_search_tool({"type": "web_search_20250305", "name": "web_search"})
        True
        >>> is_web_search_tool({"name": "calculator"})
        False
        >>> is_web_search_tool({"name": "WebSearch"})  # legacy interception marker
        True
        >>> is_web_search_tool({"name": "WebSearch", "input_schema": {"type": "object"}})  # Cowork client tool
        False
    """
    tool_name = tool.get("name", "")
    tool_type = tool.get("type", "")

    # Check for OpenAI format: {"type": "function", "function": {"name": "..."}}
    if tool_type == "function" and "function" in tool:
        function_def = tool.get("function", {})
        function_name = function_def.get("name", "")
        if function_name == LITELLM_WEB_SEARCH_TOOL_NAME:
            return True

    # Check for LiteLLM standard tool (Anthropic format)
    if tool_name == LITELLM_WEB_SEARCH_TOOL_NAME:
        return True

    # Check for native Anthropic web_search_* types
    if tool_type.startswith("web_search_"):
        return True

    # Check for Claude Code's web_search with a type field
    if tool_name == "web_search" and tool_type:
        return True

    # Legacy "WebSearch" interception marker — only when no schema is
    # present, so real client-side WebSearch tools (Cowork) pass through.
    if tool_name == "WebSearch" and "input_schema" not in tool:
        return True

    return False

