
def _format_chat_completion_stream_output(
    line: str,
) -> ChatCompletionStreamOutput | None:
    if not line.startswith("data:"):
        return None  # empty line

    if line.strip() == "data: [DONE]":
        raise StopIteration("[DONE] signal received.")

    # Decode payload
    json_payload = json.loads(line.lstrip("data:").strip())

    # Either an error as being returned
    if json_payload.get("error") is not None:
        raise _parse_text_generation_error(json_payload["error"], json_payload.get("error_type"))

    # Or parse token payload
    return ChatCompletionStreamOutput.parse_obj_as_instance(json_payload)

