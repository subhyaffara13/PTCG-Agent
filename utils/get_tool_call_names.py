
def get_tool_call_names(tools: List[ChatCompletionToolParam]) -> List[str]:
    """
    Get tool call names from tools
    """
    tool_call_names: List[str] = []
    for tool in tools:
        if tool.get("type") == "function":
            tool_call_name = tool.get("function", {}).get("name")
            if tool_call_name:
                tool_call_names.append(tool_call_name)
    return tool_call_names

