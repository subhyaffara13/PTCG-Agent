
def _extract_tools(
    model_parameters: Mapping[str, object],
) -> tuple[ToolDefinition, ...]:
    """Pull declared tools from request params (OpenAI / Anthropic shape).

    Accepts the chat-completion ``tools=[{"type":"function", "function":
    {...}}, ...]`` shape, and falls back to the ``functions=[...]`` shape.
    Returns an empty tuple when neither is present.
    """
    raw_tools = model_parameters.get("tools")
    if not isinstance(raw_tools, list):
        raw_tools = model_parameters.get("functions")  # ``functions`` shape
    if not isinstance(raw_tools, list):
        return ()
    return tuple(t for entry in raw_tools if (t := _tool_from_entry(entry)) is not None)

