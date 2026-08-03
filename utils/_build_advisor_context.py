from typing import Any, Dict, List

def _build_advisor_context(
    messages: List[Dict],
    executor_response: Any,
    advisor_use_block: Dict,
) -> List[Dict]:
    """
    Build the message list for the advisor sub-call.

    Passes the full conversation + any text the executor produced so far, then
    poses the advisor question as the last user turn.

    tool_use blocks are excluded because Anthropic requires tool_use to be
    immediately followed by tool_result — not the advisor question.
    """
    question = (advisor_use_block.get("input") or {}).get("question") or (
        "Please provide guidance on the current task."
    )
    raw_content = (
        executor_response.get("content") if isinstance(executor_response, dict) else []
    ) or []
    # Keep only text blocks — strip tool_use and provider-specific fields.
    executor_text_blocks = [
        {k: v for k, v in block.items() if k not in _PROVIDER_SPECIFIC_KEYS}
        for block in raw_content
        if isinstance(block, dict) and block.get("type") == "text"
    ]
    result = list(messages)
    if executor_text_blocks:
        result.append({"role": "assistant", "content": executor_text_blocks})
    result.append({"role": "user", "content": question})
    return result

