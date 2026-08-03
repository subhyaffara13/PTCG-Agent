import json

def parse_function_tool_arguments(
    *, input_tools: list[ChatCompletionToolUnionParam], function: Function | ParsedFunction
) -> object | None:
    input_tool = get_input_tool_by_name(input_tools=input_tools, name=function.name)
    if not input_tool:
        return None

    input_fn = cast(object, input_tool.get("function"))
    if isinstance(input_fn, PydanticFunctionTool):
        return model_parse_json(input_fn.model, function.arguments)

    input_fn = cast(FunctionDefinition, input_fn)

    if not input_fn.get("strict"):
        return None

    return json.loads(function.arguments)  # type: ignore[no-any-return]


def parse_function_tool_arguments(
    *,
    input_tools: Iterable[ToolParam] | Omit | None,
    function_call: ParsedResponseFunctionToolCall | ResponseFunctionToolCall,
) -> object:
    if input_tools is None or not is_given(input_tools):
        return None

    input_tool = get_input_tool_by_name(input_tools=input_tools, name=function_call.name)
    if not input_tool:
        return None

    tool = cast(object, input_tool)
    if isinstance(tool, ResponsesPydanticFunctionTool):
        return model_parse_json(tool.model, function_call.arguments)

    if not input_tool.get("strict"):
        return None

    return json.loads(function_call.arguments)

