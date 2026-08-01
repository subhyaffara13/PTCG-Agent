
def get_input_tool_by_name(
    *, input_tools: list[ChatCompletionToolUnionParam], name: str
) -> ChatCompletionFunctionToolParam | None:
    return next((t for t in input_tools if t["type"] == "function" and t.get("function", {}).get("name") == name), None)


def get_input_tool_by_name(*, input_tools: Iterable[ToolParam], name: str) -> FunctionToolParam | None:
    for tool in input_tools:
        if tool["type"] == "function" and tool.get("name") == name:
            return tool

    return None

