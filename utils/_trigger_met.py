from typing import Any, Dict, List, Optional, Tuple

def _trigger_met(
    trigger: Dict[str, Any],
    model: str,
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict[str, Any]]],
) -> Tuple[bool, Optional[int]]:
    """Return (trigger_met, input_tokens if counted for reuse)."""
    trigger_type = trigger.get("type", "input_tokens")
    threshold = trigger.get("value")

    if trigger_type == "tool_uses":
        if not isinstance(threshold, int):
            return False, None
        return _count_tool_uses(messages) > threshold, None

    if not isinstance(threshold, int):
        threshold = DEFAULT_INPUT_TOKENS_TRIGGER
    current_tokens = litellm.token_counter(
        model=model,
        messages=messages,
        tools=cast(Any, tools),
    )
    verbose_logger.debug(
        f"context_management polyfill: current_tokens: {current_tokens}"
    )
    verbose_logger.debug(f"context_management polyfill: threshold: {threshold}")
    return current_tokens > threshold, current_tokens

