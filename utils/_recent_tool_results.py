from typing import Any, Dict, List, Optional

def _recent_tool_results(
    messages: Optional[List[Dict[str, Any]]],
) -> List[Dict[str, Any]]:
    """Extract the current turn's tool result payloads from the request messages.

    Tool results are `role == "tool"` messages that sit at the tail of the
    conversation — i.e. after the most recent assistant message with
    `tool_calls`, waiting for the model to produce a user-facing reply. Walk
    backwards from the end and collect the contiguous run of tool messages;
    stop at the first non-tool message.

    Each result is normalized to `{content, is_error}` — the only fields
    `signals._detect_failure` / `_detect_exhaustion` actually read.
    """
    if not messages:
        return []
    results: List[Dict[str, Any]] = []
    for msg in reversed(messages):
        if not isinstance(msg, dict):
            break
        if msg.get("role") != "tool":
            break
        content = msg.get("content")
        # Some providers (Anthropic-style) carry an explicit error flag; OpenAI
        # tool results don't, so fall back to an empty/missing content heuristic
        # inside `_detect_failure`.
        is_error = bool(msg.get("is_error"))
        results.append({"content": content, "is_error": is_error})
    results.reverse()
    return results

