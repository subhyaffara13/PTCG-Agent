
def _convert_mcp_tool_choice_to_openai(
    tool_choice: Optional["ToolChoice"],
) -> Optional[Union[str, Dict[str, Any]]]:
    """
    Convert MCP ToolChoice to OpenAI tool_choice format.
    MCP: {mode: "auto"} | {mode: "required"} | {mode: "none"}
    OpenAI: "auto" | "required" | "none"
    """
    if not tool_choice:
        return None
    mode = getattr(tool_choice, "mode", "auto")
    if mode == "auto":
        return "auto"
    elif mode == "required":
        return "required"
    elif mode == "none":
        return "none"
    return "auto"

