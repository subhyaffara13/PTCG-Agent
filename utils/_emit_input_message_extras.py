
def _emit_input_message_extras(span: "Span", prefix: str, message: dict) -> None:
    """Emit additive attributes for an input message:

    - `MESSAGE_NAME` and `MESSAGE_TOOL_CALL_ID` (commonly set on tool-result
      messages so traces show which tool produced which result).
    - `MESSAGE_TOOL_CALLS.*` when an assistant message requested tools.
    - `MESSAGE_CONTENTS.*` structured content for list-shaped content
      (multimodal text + image parts). The plain `MESSAGE_CONTENT` write is
      still performed by the caller, so renderers that only read the legacy
      key continue to work.
    """
    if not isinstance(message, dict):
        return

    name = message.get("name")
    if name:
        safe_set_attribute(span, f"{prefix}.{MessageAttributes.MESSAGE_NAME}", name)

    tool_call_id = message.get("tool_call_id")
    if tool_call_id:
        safe_set_attribute(
            span,
            f"{prefix}.{MessageAttributes.MESSAGE_TOOL_CALL_ID}",
            tool_call_id,
        )

    _emit_message_tool_calls(span, prefix, message)

    content = message.get("content")
    if isinstance(content, list):
        contents_prefix = f"{prefix}.{MessageAttributes.MESSAGE_CONTENTS}"
        for part_idx, part in enumerate(content):
            if not isinstance(part, dict):
                continue
            part_prefix = f"{contents_prefix}.{part_idx}"
            part_type = part.get("type")
            if part_type in ("text", "input_text"):
                text = part.get("text")
                if isinstance(text, str):
                    safe_set_attribute(
                        span,
                        f"{part_prefix}.{MessageContentAttributes.MESSAGE_CONTENT_TYPE}",
                        "text",
                    )
                    safe_set_attribute(
                        span,
                        f"{part_prefix}.{MessageContentAttributes.MESSAGE_CONTENT_TEXT}",
                        text,
                    )
            elif part_type in ("image_url", "image", "input_image"):
                url = None
                image = part.get("image_url")
                if isinstance(image, dict):
                    url = image.get("url")
                elif isinstance(image, str):
                    url = image
                if not url:
                    # Anthropic-style source.{type=base64,media_type,data}
                    source = part.get("source")
                    if isinstance(source, dict) and source.get("data"):
                        media_type = source.get("media_type", "image/jpeg")
                        url = f"data:{media_type};base64,{source['data']}"
                    elif isinstance(part.get("url"), str):
                        url = part["url"]
                if url:
                    safe_set_attribute(
                        span,
                        f"{part_prefix}.{MessageContentAttributes.MESSAGE_CONTENT_TYPE}",
                        "image",
                    )
                    safe_set_attribute(
                        span,
                        f"{part_prefix}.message_content.image.image.url",
                        url,
                    )

