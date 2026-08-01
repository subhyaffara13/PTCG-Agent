
def adapt_tools_to_openai_standard(
    tools: List[OCIToolCall],
) -> List[ChatCompletionMessageToolCall]:
    """Convert OCI tool-call objects in a response to the OpenAI format."""
    return [
        ChatCompletionMessageToolCall(
            id=tool.id or _synthesize_oci_tool_call_id(i, tool.name, tool.arguments),
            type="function",
            function={"name": tool.name, "arguments": tool.arguments},
        )
        for i, tool in enumerate(tools)
    ]

