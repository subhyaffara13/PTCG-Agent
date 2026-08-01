
def _convert_openai_response_to_mcp_result(
    response: Any,
    model_name: str,
) -> Union["CreateMessageResult", "CreateMessageResultWithTools", "ErrorData"]:
    """
    Convert a litellm completion response to MCP CreateMessageResult.
    Args:
        response: The litellm ModelResponse.
        model_name: The model that was used.
    Returns:
        MCP CreateMessageResult or CreateMessageResultWithTools.
    """
    if not response.choices:
        verbose_logger.warning(
            "MCP sampling: LLM returned empty choices list for model=%s "
            "(possible content filter or provider error)",
            model_name,
        )
        return ErrorData(
            code=-1,
            message=(
                f"LLM returned no choices for model '{model_name}'. "
                "This may indicate content filtering or a provider-side error."
            ),
        )
    choice = response.choices[0]
    message = choice.message
    # Determine stop reason
    finish_reason = getattr(choice, "finish_reason", "stop")
    if finish_reason == "tool_calls":
        stop_reason = "toolUse"
    elif finish_reason == "length":
        stop_reason = "maxTokens"
    else:
        stop_reason = "endTurn"
    actual_model = getattr(response, "model", model_name) or model_name
    # Check if response has tool calls
    tool_calls = getattr(message, "tool_calls", None)
    if tool_calls:
        # Build ToolUseContent items
        content_parts: "List[Any]" = []
        # Include text content if present
        if message.content:
            content_parts.append(TextContent(type="text", text=message.content))
        # Convert tool calls to MCP ToolUseContent
        for tc in tool_calls:
            import json

            tool_input = tc.function.arguments
            if isinstance(tool_input, str):
                try:
                    tool_input = json.loads(tool_input)
                except (json.JSONDecodeError, TypeError):
                    tool_input = {"raw": tool_input}
            content_parts.append(
                ToolUseContent(
                    type="tool_use",
                    id=tc.id,
                    name=tc.function.name,
                    input=tool_input,
                )
            )
        return CreateMessageResultWithTools(
            role="assistant",
            content=content_parts,
            model=actual_model,
            stopReason=stop_reason,
        )
    # Simple text response
    text = message.content or ""
    return CreateMessageResult(
        role="assistant",
        content=TextContent(type="text", text=text),
        model=actual_model,
        stopReason=stop_reason,
    )

