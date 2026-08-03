from typing import Any, Dict, List, Optional, Tuple

def _slice_around_compaction_block(
    messages: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """Apply Anthropic's "drop everything before the compaction block" rule.

    Returns ``(sliced_messages_with_compaction_block, compaction_block_dict)``
    if a block was found, else ``(original_messages, None)``. The sliced result
    keeps the compaction block in the assistant turn that originally carried
    it (in practice it's the only block in that turn) so callers can still
    extract the summary text from it.
    """
    msg_idx, blk_idx = _find_latest_compaction_index(messages)
    if msg_idx is None or blk_idx is None:
        return messages, None

    original_msg = messages[msg_idx]
    original_content = original_msg["content"]
    compaction_block = cast(Dict[str, Any], original_content[blk_idx])

    # Per Anthropic's contract everything before the compaction block is
    # dropped, including earlier blocks within the same assistant message.
    sliced_content = list(original_content[blk_idx:])
    sliced_first_msg = {**original_msg, "content": sliced_content}

    sliced_messages: List[Dict[str, Any]] = [sliced_first_msg]
    sliced_messages.extend(messages[msg_idx + 1 :])
    return sliced_messages, compaction_block

