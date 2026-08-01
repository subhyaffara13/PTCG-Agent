
def validate_input_tools(
    tools: Iterable[ChatCompletionToolUnionParam] | Omit = omit,
) -> Iterable[ChatCompletionFunctionToolParam] | Omit:
    if not is_given(tools):
        return omit

    for tool in tools:
        if tool["type"] != "function":
            raise ValueError(
                f"Currently only `function` tool types support auto-parsing; Received `{tool['type']}`",
            )

        strict = tool["function"].get("strict")
        if strict is not True:
            raise ValueError(
                f"`{tool['function']['name']}` is not strict. Only `strict` function tools can be auto-parsed"
            )

    return cast(Iterable[ChatCompletionFunctionToolParam], tools)

