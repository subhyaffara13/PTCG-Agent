
def _stream_chat_completion_response(
    lines: Iterable[str],
) -> Iterable[ChatCompletionStreamOutput]:
    """Used in `InferenceClient.chat_completion` if model is served with TGI."""
    for line in lines:
        try:
            output = _format_chat_completion_stream_output(line)
        except StopIteration:
            break
        if output is not None:
            yield output

