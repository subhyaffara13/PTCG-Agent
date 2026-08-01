
def has_code_execution_tool(tools: Optional[List[Dict]]) -> bool:
    """Check if litellm_code_execution tool is in the tools list."""
    if not tools:
        return False
    for tool in tools:
        func = tool.get("function", {})
        if func.get("name") == LiteLLMInternalTools.CODE_EXECUTION.value:
            return True
    return False

