
def get_litellm_web_search_tool_openai() -> Dict[str, Any]:
    """
    Get the standard LiteLLM web search tool definition in OpenAI format.

    Used by async_pre_call_deployment_hook which runs in the chat completions
    path where tools must be in OpenAI format (type: "function" with
    function.parameters).

    Returns:
        Dict containing the OpenAI-style tool definition.
    """
    return {
        "type": "function",
        "function": {
            "name": LITELLM_WEB_SEARCH_TOOL_NAME,
            "description": (
                "Search the web for information. Use this when you need current "
                "information or answers to questions that require up-to-date data."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to execute",
                    }
                },
                "required": ["query"],
            },
        },
    }

