from typing import Any, Dict, List

def _select_last_user_question(
    messages: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Pick the most recent ``user`` turn that is a real question.

    Returns a one-element message list with any ``tool_result`` blocks
    stripped: after compaction the paired ``tool_use`` assistant turn no
    longer exists in the downstream context, so forwarding ``tool_result``
    blocks would translate to orphaned ``role=tool`` messages on
    non-Anthropic providers (OpenAI, Gemini, …) and cause a 400 error.

    Falls back to a synthetic continuation prompt if no eligible turn
    exists (e.g. the conversation only ever contained ``tool_result``
    turns, or contained no user turns at all). The downstream call always
    needs a non-empty user message.
    """
    for msg in reversed(messages):
        if msg.get("role") != "user":
            continue
        content = msg.get("content")
        if isinstance(content, list):
            filtered = [
                blk
                for blk in content
                if not (isinstance(blk, dict) and blk.get("type") == "tool_result")
            ]
            if not filtered:
                # Purely tool_result — skip and look for an earlier turn.
                continue
            if len(filtered) < len(content):
                return [{**msg, "content": filtered}]
        return [msg]
    return [
        {
            "role": "user",
            "content": "Please continue based on the conversation summary above.",
        }
    ]

