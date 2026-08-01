
def select_strict_chat_completion_tools(
    tools: Iterable[ChatCompletionToolUnionParam] | Omit = omit,
) -> Iterable[ChatCompletionFunctionToolParam] | Omit:
    """Select only the strict ChatCompletionFunctionToolParams from the given tools."""
    if not is_given(tools):
        return omit

    return [t for t in tools if is_strict_chat_completion_tool_param(t)]

