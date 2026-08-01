
def _strip_compaction_blocks(
    messages: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Drop any ``compaction`` content blocks from messages.

    Used to build the downstream-bound message list — the adapter has no
    concept of a compaction block, so it must not see one.
    """
    cleaned: List[Dict[str, Any]] = []
    for msg in messages:
        content = msg.get("content")
        if not isinstance(content, list):
            cleaned.append(msg)
            continue
        filtered = [
            block
            for block in content
            if not (isinstance(block, dict) and block.get("type") == "compaction")
        ]
        if not filtered:
            # The compaction block was the only content; drop the whole turn.
            continue
        cleaned.append({**msg, "content": filtered})
    return cleaned

