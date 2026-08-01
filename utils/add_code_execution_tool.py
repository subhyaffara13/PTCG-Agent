
def add_code_execution_tool(tools: Optional[List[Dict]]) -> List[Dict]:
    """Add litellm_code_execution tool if not already present."""
    tools = tools or []
    if not has_code_execution_tool(tools):
        tools.append(LITELLM_CODE_EXECUTION_TOOL)
    return tools

