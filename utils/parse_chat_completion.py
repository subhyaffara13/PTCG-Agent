
def parse_chat_completion(
    *,
    response_format: type[ResponseFormatT] | completion_create_params.ResponseFormat | Omit,
    input_tools: Iterable[ChatCompletionToolUnionParam] | Omit,
    chat_completion: ChatCompletion | ParsedChatCompletion[object],
) -> ParsedChatCompletion[ResponseFormatT]:
    if is_given(input_tools):
        input_tools = [t for t in input_tools]
    else:
        input_tools = []

    choices: list[ParsedChoice[ResponseFormatT]] = []
    for choice in chat_completion.choices:
        if choice.finish_reason == "length":
            raise LengthFinishReasonError(completion=chat_completion)

        if choice.finish_reason == "content_filter":
            raise ContentFilterFinishReasonError()

        message = choice.message

        tool_calls: list[ParsedFunctionToolCall] = []
        if message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.type == "function":
                    tool_call_dict = tool_call.to_dict()
                    tool_calls.append(
                        construct_type_unchecked(
                            value={
                                **tool_call_dict,
                                "function": {
                                    **cast(Any, tool_call_dict["function"]),
                                    "parsed_arguments": parse_function_tool_arguments(
                                        input_tools=input_tools, function=tool_call.function
                                    ),
                                },
                            },
                            type_=ParsedFunctionToolCall,
                        )
                    )
                elif tool_call.type == "custom":
                    # warn user that custom tool calls are not callable here
                    log.warning(
                        "Custom tool calls are not callable. Ignoring tool call: %s - %s",
                        tool_call.id,
                        tool_call.custom.name,
                        stacklevel=2,
                    )
                elif TYPE_CHECKING:  # type: ignore[unreachable]
                    assert_never(tool_call)
                else:
                    tool_calls.append(tool_call)

        choices.append(
            construct_type_unchecked(
                type_=ParsedChoice[ResponseFormatT],
                value={
                    **choice.to_dict(),
                    "message": {
                        **message.to_dict(),
                        "parsed": maybe_parse_content(
                            response_format=response_format,
                            message=message,
                        ),
                        "tool_calls": tool_calls if tool_calls else None,
                    },
                },
            )
        )

    return construct_type_unchecked(
        type_=ParsedChatCompletion[ResponseFormatT],
        value={
            **chat_completion.to_dict(),
            "choices": choices,
        },
    )

