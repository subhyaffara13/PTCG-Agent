from typing import Any, Dict, List, Union

def _convert_single_content(
    content: Any,
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """Convert a single MCP content item to OpenAI format.

    For text/image/audio content, returns a single content-part dict.
    For tool_use/tool_result, returns a dict with a ``_marker_type`` key
    so the caller (``_convert_mcp_messages_to_openai``) can hoist it to
    the correct message-level position (``tool_calls`` array or a
    separate ``role: "tool"`` message).
    """
    import json

    content_type = getattr(content, "type", None)
    if content_type == "text":
        return {"type": "text", "text": content.text}
    elif content_type == "image":
        data = getattr(content, "data", "")
        mime_type = getattr(content, "mimeType", "image/png")
        return {
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{data}"},
        }
    elif content_type == "audio":
        data = getattr(content, "data", "")
        mime_type = getattr(content, "mimeType", "audio/wav")
        # Map MIME type to OpenAI audio format
        format_map = {
            "audio/wav": "wav",
            "audio/mp3": "mp3",
            "audio/mpeg": "mp3",
            "audio/flac": "flac",
            "audio/ogg": "ogg",
        }
        audio_format = format_map.get(mime_type, "wav")
        return {
            "type": "input_audio",
            "input_audio": {"data": data, "format": audio_format},
        }
    elif content_type == "tool_use":
        # ToolUseContent → proper OpenAI function-call representation.
        # The ``_marker_type`` key lets the message-level converter
        # hoist this into the ``tool_calls`` array on the assistant
        # message instead of embedding it inline as a content part.
        return {
            "_marker_type": "tool_use",
            "id": getattr(content, "id", f"call_{id(content)}"),
            "type": "function",
            "function": {
                "name": getattr(content, "name", ""),
                "arguments": json.dumps(getattr(content, "input", {}), default=str),
            },
        }
    elif content_type == "tool_result":
        # ToolResultContent → proper OpenAI tool-role message.
        # Marked so the message-level converter can emit it as a
        # separate ``{"role": "tool", ...}`` message.
        tool_use_id = getattr(content, "toolUseId", "")
        nested_content = getattr(content, "content", [])
        if isinstance(nested_content, list):
            text_parts = [
                getattr(c, "text", str(c))
                for c in nested_content
                if getattr(c, "type", None) == "text"
            ]
            result_text = "\n".join(text_parts) if text_parts else ""
        else:
            result_text = str(nested_content)
        return {
            "_marker_type": "tool_result",
            "role": "tool",
            "tool_call_id": tool_use_id,
            "content": result_text,
        }
    # Fallback: treat as text
    return {"type": "text", "text": str(content)}

