
def remove_custom_field_from_tools(request_body: dict) -> None:
    """
    Remove ``custom`` field from each tool in the request body.

    Claude Code (v2.1.69+) sends ``custom: {defer_loading: true}`` on tool
    definitions, which Anthropic's API accepts but Bedrock rejects with
    ``"Extra inputs are not permitted"``.

    Args:
        request_body: The request dictionary to modify in-place.

    Ref: https://github.com/BerriAI/litellm/issues/22847
    """
    tools = request_body.get("tools")
    if not tools or not isinstance(tools, list):
        return
    for tool in tools:
        if isinstance(tool, dict):
            tool.pop("custom", None)

