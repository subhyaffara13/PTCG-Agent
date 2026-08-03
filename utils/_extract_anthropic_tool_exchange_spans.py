from typing import List, Optional, Set, Tuple

def _extract_anthropic_tool_exchange_spans(
    messages: List[dict],
) -> Tuple[List[Set[int]], Optional[str]]:
    """
    Return atomic 2-message spans for Anthropic tool exchanges.

    Each assistant message containing `tool_use` must be immediately followed by a
    user message containing matching `tool_result` blocks for all tool_use ids.
    """
    spans: List[Set[int]] = []
    i = 0
    while i < len(messages):
        current = messages[i]
        if current.get("role") != "assistant":
            i += 1
            continue

        tool_use_ids = _extract_tool_use_ids(current.get("content"))
        if not tool_use_ids:
            i += 1
            continue

        if i + 1 >= len(messages):
            return [], "invalid_anthropic_tool_sequence"

        next_msg = messages[i + 1]
        if next_msg.get("role") != "user":
            return [], "invalid_anthropic_tool_sequence"

        tool_result_ids = _extract_tool_result_ids(next_msg.get("content"))
        if not tool_result_ids:
            return [], "invalid_anthropic_tool_sequence"

        for tool_use_id in tool_use_ids:
            if tool_use_id not in tool_result_ids:
                return [], "invalid_anthropic_tool_sequence"

        spans.append({i, i + 1})
        i += 2

    return spans, None

