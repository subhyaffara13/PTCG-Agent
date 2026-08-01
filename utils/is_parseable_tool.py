
def is_parseable_tool(input_tool: ChatCompletionToolUnionParam) -> bool:
    if input_tool["type"] != "function":
        return False

    input_fn = cast(object, input_tool.get("function"))
    if isinstance(input_fn, PydanticFunctionTool):
        return True

    return cast(FunctionDefinition, input_fn).get("strict") or False

