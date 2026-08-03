import json

def _format_text_generation_stream_output(line: str, details: bool) -> str | TextGenerationStreamOutput | None:
    if not line.startswith("data:"):
        return None  # empty line

    if line.strip() == "data: [DONE]":
        raise StopIteration("[DONE] signal received.")

    # Decode payload
    payload = line.lstrip("data:").rstrip("/n")
    json_payload = json.loads(payload)

    # Either an error as being returned
    if json_payload.get("error") is not None:
        raise _parse_text_generation_error(json_payload["error"], json_payload.get("error_type"))

    # Or parse token payload
    output = TextGenerationStreamOutput.parse_obj_as_instance(json_payload)
    return output.token.text if not details else output

