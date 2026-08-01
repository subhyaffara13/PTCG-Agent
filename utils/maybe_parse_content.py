
def maybe_parse_content(
    *,
    response_format: type[ResponseFormatT] | ResponseFormatParam | Omit,
    message: ChatCompletionMessage | ParsedChatCompletionMessage[object],
) -> ResponseFormatT | None:
    if has_rich_response_format(response_format) and message.content and not message.refusal:
        return _parse_content(response_format, message.content)

    return None

