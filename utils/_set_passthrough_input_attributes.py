
def _set_passthrough_input_attributes(span: "Span", messages) -> None:
    """Render passthrough request messages into INPUT_VALUE + LLM_INPUT_MESSAGES."""
    if not (isinstance(messages, list) and messages):
        return
    # Set INPUT_VALUE from the last user message text if discoverable.
    last_text = None
    for msg in reversed(messages):
        if isinstance(msg, dict):
            last_text = _coerce_text(msg.get("content"))
            if last_text:
                break
    if last_text:
        safe_set_attribute(span, SpanAttributes.INPUT_VALUE, last_text)
    # Mirror messages into LLM_INPUT_MESSAGES so the input pane renders.
    for idx, msg in enumerate(messages):
        if not isinstance(msg, dict):
            continue
        prefix = f"{SpanAttributes.LLM_INPUT_MESSAGES}.{idx}"
        role = msg.get("role")
        if role:
            safe_set_attribute(
                span,
                f"{prefix}.{MessageAttributes.MESSAGE_ROLE}",
                role,
            )
        text = _coerce_text(msg.get("content"))
        if text is not None:
            safe_set_attribute(
                span,
                f"{prefix}.{MessageAttributes.MESSAGE_CONTENT}",
                text,
            )

