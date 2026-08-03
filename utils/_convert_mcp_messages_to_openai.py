from typing import Any, Dict, List, Optional

def _convert_mcp_messages_to_openai(
    messages: List["SamplingMessage"],
    system_prompt: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Convert MCP SamplingMessage list to OpenAI messages format.
    MCP messages use:
    - role: "user" | "assistant"
    - content: TextContent | ImageContent | AudioContent | ToolUseContent
              | ToolResultContent | list[...]
    OpenAI messages use:
    - role: "system" | "user" | "assistant" | "tool"
    - content: str | list[content_part]
    """
    openai_messages: List[Dict[str, Any]] = []
    # Add system prompt if provided
    if system_prompt:
        openai_messages.append({"role": "system", "content": system_prompt})
    for msg in messages:
        role = msg.role
        content = msg.content
        # Handle tool use content from assistant
        if role == "assistant" and _has_tool_use(content):
            tool_calls = _extract_tool_calls(content)
            if tool_calls:
                openai_msg: Dict[str, Any] = {
                    "role": "assistant",
                    "tool_calls": tool_calls,
                }
                # Also include any text content alongside tool calls
                text_parts = _extract_text_parts(content)
                if text_parts:
                    openai_msg["content"] = text_parts
                openai_messages.append(openai_msg)
                continue
        # Handle tool result content from user
        if role == "user" and _has_tool_result(content):
            tool_results = _extract_tool_results(content)
            for tool_result in tool_results:
                openai_messages.append(tool_result)
            continue
        # Standard text/image/audio message — also handles any stray
        # tool_use / tool_result that slipped past the fast-path checks
        # above (e.g. unexpected role, single non-list content).
        converted = _convert_mcp_content_to_openai(content)
        converted_parts = (
            converted
            if isinstance(converted, list)
            else ([converted] if isinstance(converted, dict) else [])
        )

        # Separate marker items from regular content parts
        tool_call_markers = []
        tool_result_markers = []
        regular_parts = []
        for part in converted_parts:
            marker = part.get("_marker_type") if isinstance(part, dict) else None
            if marker == "tool_use":
                # Strip the internal marker before emitting
                tc = {k: v for k, v in part.items() if k != "_marker_type"}
                tool_call_markers.append(tc)
            elif marker == "tool_result":
                tr = {k: v for k, v in part.items() if k != "_marker_type"}
                tool_result_markers.append(tr)
            else:
                regular_parts.append(part)

        # Emit assistant message with tool_calls if any were found
        if tool_call_markers:
            openai_msg_tc: Dict[str, Any] = {
                "role": "assistant",
                "tool_calls": tool_call_markers,
            }
            if regular_parts:
                openai_msg_tc["content"] = regular_parts
            openai_messages.append(openai_msg_tc)
        elif regular_parts:
            if isinstance(converted, str):
                openai_messages.append({"role": role, "content": converted})
            else:
                openai_messages.append({"role": role, "content": regular_parts})

        # Emit separate tool-result messages
        for tr in tool_result_markers:
            openai_messages.append(tr)

    return openai_messages

