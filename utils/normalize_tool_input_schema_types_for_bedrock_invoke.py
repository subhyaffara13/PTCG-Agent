
def normalize_tool_input_schema_types_for_bedrock_invoke(request_body: dict) -> None:
    """
    Bedrock Invoke (Anthropic Messages) validates ``input_schema`` as JSON Schema.
    Anthropic's API allows ``type: \"custom\"`` for Claude Code custom tools; Bedrock
    rejects it with: ``tools.0.custom.input_schema.type: Input should be 'object'``.

    Normalizes ``type: \"custom\"`` to ``\"object\"`` throughout each tool's
    ``input_schema`` (recursive for nested properties, items, combinators).

    Args:
        request_body: Request dictionary to modify in-place.
    """
    tools = request_body.get("tools")
    if not tools or not isinstance(tools, list):
        return
    for tool in tools:
        if not isinstance(tool, dict):
            continue
        input_schema = tool.get("input_schema")
        if isinstance(input_schema, dict):
            normalize_json_schema_custom_types_to_object(input_schema)

