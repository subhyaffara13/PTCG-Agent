
def ensure_bedrock_anthropic_messages_tool_names(request_body: dict) -> None:
    """
    Bedrock Invoke (Anthropic Messages) requires each tool to include ``name``.
    Some clients send only ``input_schema``; Bedrock then errors with
    ``tools.0.custom.name: Field required``.

    In-place: set ``name`` to ``litellm_unnamed_tool_{index}`` when missing or blank.
    """
    tools = request_body.get("tools")
    if not tools or not isinstance(tools, list):
        return
    for i, tool in enumerate(tools):
        if not isinstance(tool, dict):
            continue
        name = tool.get("name")
        if name is None or (isinstance(name, str) and not name.strip()):
            tool["name"] = f"litellm_unnamed_tool_{i}"

