
def _resolve_trigger_tokens(edit_spec: Dict[str, Any]) -> Tuple[int, List[str]]:
    """Validate and resolve ``trigger.value``.

    Raises ``AnthropicContextManagementError`` if the explicitly-supplied value
    is below the 50k minimum. Unknown ``trigger.type`` values fall back to
    ``input_tokens`` with a warning.
    """
    warnings: List[str] = []
    trigger = edit_spec.get("trigger") or {}
    if not isinstance(trigger, dict):
        warnings.append("trigger_not_a_dict_using_default")
        return COMPACT_DEFAULT_TRIGGER_TOKENS, warnings

    trigger_type = trigger.get("type", "input_tokens")
    if trigger_type != "input_tokens":
        warnings.append(f"unsupported_trigger_type_{trigger_type}_using_input_tokens")

    value = trigger.get("value")
    if value is None:
        return COMPACT_DEFAULT_TRIGGER_TOKENS, warnings
    if not isinstance(value, int):
        warnings.append("trigger_value_not_int_using_default")
        return COMPACT_DEFAULT_TRIGGER_TOKENS, warnings
    if value < COMPACT_MIN_TRIGGER_TOKENS:
        raise AnthropicContextManagementError(
            status_code=400,
            message=(
                f"context_management.compact_20260112.trigger.value must be at "
                f"least {COMPACT_MIN_TRIGGER_TOKENS} tokens"
            ),
        )
    return value, warnings

