
def has_parseable_input(
    *,
    response_format: type | ResponseFormatParam | Omit,
    input_tools: Iterable[ChatCompletionToolUnionParam] | Omit = omit,
) -> bool:
    if has_rich_response_format(response_format):
        return True

    for input_tool in input_tools or []:
        if is_parseable_tool(input_tool):
            return True

    return False

