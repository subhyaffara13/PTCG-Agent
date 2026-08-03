from typing import Any, Dict, List, Optional, Tuple

def apply_clear_tool_uses_20250919(
    *,
    model: str,
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]],
    system: Any,
    edit_spec: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], Optional[AppliedEdit]]:
    """Apply clear_tool_uses; return (messages, AppliedEdit or None)."""
    ignored_knobs = [
        knob
        for knob in ("clear_at_least", "exclude_tools", "clear_tool_inputs")
        if knob in edit_spec
    ]
    for ignored_knob in ignored_knobs:
        verbose_logger.warning(
            "context_management polyfill: ignoring '%s' on %s "
            "(supported only on Anthropic-family forwarding path in v0)",
            ignored_knob,
            CLEAR_TOOL_USES_EDIT_TYPE,
        )

    trigger = edit_spec.get("trigger") or {
        "type": "input_tokens",
        "value": DEFAULT_INPUT_TOKENS_TRIGGER,
    }
    keep = edit_spec.get("keep") or {
        "type": "tool_uses",
        "value": DEFAULT_KEEP_TOOL_USES,
    }

    met, tokens_before = _trigger_met(trigger, model, messages, tools)
    if not met:
        return messages, None

    keep_count = _resolve_keep_count(keep)
    tool_use_ids = _collect_tool_use_ids_in_order(messages)
    if len(tool_use_ids) <= keep_count:
        return messages, None

    ids_to_clear = set(tool_use_ids[: len(tool_use_ids) - keep_count])

    # Never clear the latest completed tool_result (reply context).
    last_completed_id = _last_completed_tool_use_id(messages)
    if last_completed_id is not None:
        ids_to_clear.discard(last_completed_id)

    edited, cleared_count = _clear_tool_results(messages, ids_to_clear)
    verbose_logger.debug("context_management polyfill: edited: %s", edited)
    if cleared_count == 0:
        return messages, None

    if tokens_before is None:
        tokens_before = litellm.token_counter(
            model=model, messages=messages, tools=cast(Any, tools)
        )
    tokens_after = litellm.token_counter(
        model=model, messages=edited, tools=cast(Any, tools)
    )
    cleared_input_tokens = max(tokens_before - tokens_after, 0)

    applied: AppliedEdit = {
        "type": CLEAR_TOOL_USES_EDIT_TYPE,
        "cleared_tool_uses": cleared_count,
        "cleared_input_tokens": cleared_input_tokens,
    }
    if ignored_knobs:
        applied["warnings"] = [f"{knob}_ignored" for knob in ignored_knobs]
    return edited, applied

