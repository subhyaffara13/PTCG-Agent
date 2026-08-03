import copy
from typing import Any, List

def strip_thinking_blocks_from_anthropic_messages(messages: List[Any]) -> List[Any]:
    """
    Return a new message list with thinking / redacted_thinking content blocks removed
    from each message. Used to recover from invalid thinking signatures on retry.

    Messages whose content is a list and becomes empty after stripping are omitted,
    since Anthropic rejects empty content arrays.
    """
    out: List[Any] = []
    for m in messages:
        if not isinstance(m, dict):
            out.append(m)
            continue
        mm = copy.deepcopy(m)
        content = mm.get("content")
        if isinstance(content, list):
            filtered = [
                b
                for b in content
                if not (
                    isinstance(b, dict)
                    and b.get("type") in ("thinking", "redacted_thinking")
                )
            ]
            if not filtered:
                continue
            mm["content"] = filtered
        out.append(mm)
    return out

