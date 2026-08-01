
def _emit_message_tool_calls(span: "Span", prefix: str, message) -> None:
    """Emit ``MESSAGE_TOOL_CALLS.*`` for an assistant message that requested
    tool calls. Pure addition: only writes when ``tool_calls`` is non-empty.

    Accepts dicts or Pydantic message objects (e.g. ``litellm.Message``); the
    same applies to each tool_call entry.
    """
    tool_calls = _get_tool_calls(message)
    if not tool_calls:
        return
    for tc_idx, raw_tc in enumerate(tool_calls):
        tc = _normalize_tool_call(raw_tc)
        if tc is None:
            continue
        tc_prefix = f"{prefix}.{MessageAttributes.MESSAGE_TOOL_CALLS}.{tc_idx}"
        if tc["id"]:
            safe_set_attribute(
                span, f"{tc_prefix}.{ToolCallAttributes.TOOL_CALL_ID}", tc["id"]
            )
        fn = tc["function"]
        if fn["name"]:
            safe_set_attribute(
                span,
                f"{tc_prefix}.{ToolCallAttributes.TOOL_CALL_FUNCTION_NAME}",
                fn["name"],
            )
        if fn["arguments"] is not None:
            safe_set_attribute(
                span,
                f"{tc_prefix}.{ToolCallAttributes.TOOL_CALL_FUNCTION_ARGUMENTS_JSON}",
                fn["arguments"],
            )

