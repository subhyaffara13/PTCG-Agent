
def _stream_text_generation_response(
    output_lines: Iterable[str], details: bool
) -> Iterable[str] | Iterable[TextGenerationStreamOutput]:
    """Used in `InferenceClient.text_generation`."""
    # Parse ServerSentEvents
    for line in output_lines:
        try:
            output = _format_text_generation_stream_output(line, details)
        except StopIteration:
            break
        if output is not None:
            yield output

