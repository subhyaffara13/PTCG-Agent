
def convert_function_to_anthropic_tool_invoke(
    function_call: Union[dict, ChatCompletionToolCallFunctionChunk],
) -> List[AnthropicMessagesToolUseParam]:
    try:
        _name = get_attribute_or_key(function_call, "name") or ""
        _arguments = get_attribute_or_key(function_call, "arguments")

        tool_input = parse_tool_call_arguments(
            _arguments, tool_name=_name, context="Anthropic function to tool invoke"
        )

        anthropic_tool_invoke = [
            AnthropicMessagesToolUseParam(
                type="tool_use",
                id=str(uuid.uuid4()),
                name=_name,
                input=tool_input,
            )
        ]
        return anthropic_tool_invoke
    except Exception as e:
        raise e

