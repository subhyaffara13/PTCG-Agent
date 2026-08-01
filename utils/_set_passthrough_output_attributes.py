
def _set_passthrough_output_attributes(span: "Span", parsed_response: dict) -> None:
    """Render passthrough response into OUTPUT_VALUE + LLM_OUTPUT_MESSAGES."""
    # Anthropic / Bedrock-Anthropic: `content` is a list of typed parts.
    content_list = parsed_response.get("content")
    if isinstance(content_list, list) and content_list:
        texts = []
        for part in content_list:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                texts.append(part["text"])
        joined = "\n\n".join(t for t in texts if t)
        if joined:
            safe_set_attribute(span, SpanAttributes.OUTPUT_VALUE, joined)
            prefix = f"{SpanAttributes.LLM_OUTPUT_MESSAGES}.0"
            safe_set_attribute(
                span,
                f"{prefix}.{MessageAttributes.MESSAGE_ROLE}",
                parsed_response.get("role", "assistant"),
            )
            safe_set_attribute(
                span,
                f"{prefix}.{MessageAttributes.MESSAGE_CONTENT}",
                joined,
            )

    # OpenAI-style passthrough: `choices[0].message.content`
    choices = parsed_response.get("choices")
    if isinstance(choices, list) and choices:
        first = choices[0]
        if isinstance(first, dict):
            msg = first.get("message")
            if isinstance(msg, dict):
                text = _coerce_text(msg.get("content"))
                if text:
                    safe_set_attribute(span, SpanAttributes.OUTPUT_VALUE, text)
                    prefix = f"{SpanAttributes.LLM_OUTPUT_MESSAGES}.0"
                    safe_set_attribute(
                        span,
                        f"{prefix}.{MessageAttributes.MESSAGE_ROLE}",
                        msg.get("role", "assistant"),
                    )
                    safe_set_attribute(
                        span,
                        f"{prefix}.{MessageAttributes.MESSAGE_CONTENT}",
                        text,
                    )

