
def parse_tool_calls(processor, generated_ids, schema: dict) -> list[dict] | None:
    """Parse tool calls from generated token IDs using ``tokenizer.parse_response``.

    Args:
        processor: The processor or tokenizer.
        generated_ids: Token IDs from generation. Passed directly to ``parse_response``
            which decodes them internally, preserving special tokens that
            ``skip_special_tokens=True`` would strip (e.g. Gemma's ``<|tool_call>``).
        schema: The tool call schema (from ``response_schema`` or ``_TOOL_CALL_FALLBACKS``).

    Returns a list of ``{"name": str, "arguments": str}`` dicts, or ``None`` if none found.
    """
    parsed = processor.parse_response(generated_ids, schema)
    if not parsed:
        return None
    if not isinstance(parsed, list):
        parsed = [parsed]
    tool_calls = [_normalize_tool_call(tool_call) for tool_call in parsed]
    return tool_calls if tool_calls else None


def parse_tool_calls(tool_calls):
    if tool_calls is None:
        return None

    def clean_tool_call(tool_call):
        serialized = {
            "type": tool_call.type,
            "id": tool_call.id,
            "function": {
                "name": tool_call.function.name,
                "arguments": tool_call.function.arguments,
            },
        }

        return serialized

    return [clean_tool_call(tool_call) for tool_call in tool_calls]

