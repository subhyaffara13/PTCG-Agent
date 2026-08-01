
def get_litellm_web_search_tool() -> Dict[str, Any]:
    """
    Get the standard LiteLLM web search tool definition.

    This is the canonical tool definition that all native web search tools
    (like Anthropic's web_search_20250305, Claude Code's web_search, etc.)
    are converted to for interception.

    Returns:
        Dict containing the Anthropic-style tool definition with:
        - name: Tool name
        - description: What the tool does
        - input_schema: JSON schema for tool parameters

    Example:
        >>> tool = get_litellm_web_search_tool()
        >>> tool['name']
        'litellm_web_search'
    """
    return {
        "name": LITELLM_WEB_SEARCH_TOOL_NAME,
        "description": (
            "Search the web for information. Use this when you need current "
            "information or answers to questions that require up-to-date data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to execute",
                }
            },
            "required": ["query"],
        },
    }

