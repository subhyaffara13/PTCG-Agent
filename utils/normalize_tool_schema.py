
def normalize_tool_schema(tool: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a tool's parameter schema to use standard JSON Schema lowercase types.

    Args:
        tool: The tool definition containing function parameters

    Returns:
        The tool with normalized schema types
    """
    if not isinstance(tool, dict):
        return tool

    normalized_tool = tool.copy()

    # Normalize function parameters if present
    if "function" in tool and isinstance(tool["function"], dict):
        normalized_tool["function"] = tool["function"].copy()
        if "parameters" in tool["function"]:
            normalized_tool["function"]["parameters"] = normalize_json_schema_types(
                tool["function"]["parameters"]
            )

    return normalized_tool

