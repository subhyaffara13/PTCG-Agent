
def _count_tool_uses(messages: List[Dict[str, Any]]) -> int:
    """Return the number of tool_use content blocks across all messages.

    Only counts blocks with a string ``id`` to stay consistent with
    :func:`_collect_tool_use_ids_in_order`, which is the source of truth for
    which blocks are clearable.
    """
    count = 0
    for msg in messages:
        content = msg.get("content")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "tool_use":
                    if isinstance(block.get("id"), str):
                        count += 1
    return count

