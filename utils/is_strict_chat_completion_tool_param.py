
def is_strict_chat_completion_tool_param(
    tool: ChatCompletionToolUnionParam,
) -> TypeGuard[ChatCompletionFunctionToolParam]:
    """Check if the given tool is a strict ChatCompletionFunctionToolParam."""
    if not tool["type"] == "function":
        return False
    if tool["function"].get("strict") is not True:
        return False

    return True

