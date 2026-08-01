
def _set_choice_outputs(span: "Span", response_obj, msg_attrs, span_attrs):
    for idx, choice in enumerate(response_obj.get("choices", [])):
        response_message = choice.get("message", {})
        content = response_message.get("content", "")

        # Tool-only assistant responses have empty content; serialize the
        # tool_calls into OUTPUT_VALUE so Arize's "Output" pane isn't blank.
        output_value = content
        if not output_value:
            tool_calls = _get_tool_calls(response_message)
            if tool_calls:
                output_value = _summarize_tool_calls_for_output(tool_calls)

        safe_set_attribute(span, span_attrs.OUTPUT_VALUE, output_value)
        prefix = f"{span_attrs.LLM_OUTPUT_MESSAGES}.{idx}"
        safe_set_attribute(
            span,
            f"{prefix}.{msg_attrs.MESSAGE_ROLE}",
            response_message.get("role"),
        )
        safe_set_attribute(
            span,
            f"{prefix}.{msg_attrs.MESSAGE_CONTENT}",
            content,
        )

        # Additive: emit assistant tool_calls so tool-using turns render in
        # Arize/Phoenix. Sets new MESSAGE_TOOL_CALLS keys only — does not
        # change MESSAGE_CONTENT/MESSAGE_ROLE writes above.
        _safe_emit(
            f"output tool_calls (idx={idx})",
            _emit_message_tool_calls,
            span,
            prefix,
            response_message,
        )

