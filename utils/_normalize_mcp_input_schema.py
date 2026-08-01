
def _normalize_mcp_input_schema(input_schema: dict) -> dict:
    """
    Normalize MCP input schema to ensure it's valid for OpenAI function calling.

    OpenAI requires that function parameters have:
    - type: 'object'
    - properties: dict (can be empty)
    - additionalProperties: false (recommended)
    """
    if not input_schema:
        return {"type": "object", "properties": {}, "additionalProperties": False}

    # Make a copy to avoid modifying the original
    normalized_schema = dict(input_schema)

    # Ensure type is 'object'
    if "type" not in normalized_schema:
        normalized_schema["type"] = "object"

    # Ensure properties exists (can be empty)
    if "properties" not in normalized_schema:
        normalized_schema["properties"] = {}

    # Add additionalProperties if not present (recommended by OpenAI)
    if "additionalProperties" not in normalized_schema:
        normalized_schema["additionalProperties"] = False

    return normalized_schema

