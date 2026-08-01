
def _find_latest_compaction_index(
    messages: List[Dict[str, Any]],
) -> Tuple[Optional[int], Optional[int]]:
    """Return (message_index, block_index) of the most recent compaction block.

    ``None, None`` if no compaction block is present. Iterates from the end so
    only the latest one is considered.
    """
    for msg_idx in range(len(messages) - 1, -1, -1):
        content = messages[msg_idx].get("content")
        if not isinstance(content, list):
            continue
        for blk_idx in range(len(content) - 1, -1, -1):
            block = content[blk_idx]
            if isinstance(block, dict) and block.get("type") == "compaction":
                return msg_idx, blk_idx
    return None, None

