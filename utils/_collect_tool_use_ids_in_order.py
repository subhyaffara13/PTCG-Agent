
def _collect_tool_use_ids_in_order(messages: List[Dict[str, Any]]) -> List[str]:
    """Return tool_use ids in the chronological order they appear in messages."""
    ids: List[str] = []
    for msg in messages:
        content = msg.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    block_id = block.get("id")
                    if isinstance(block_id, str):
                        ids.append(block_id)
    return ids

