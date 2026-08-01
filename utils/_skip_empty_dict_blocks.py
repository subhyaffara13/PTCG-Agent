
def _skip_empty_dict_blocks(blocks: List[dict]) -> List[dict]:
    """
    Filter out empty text blocks from a list of dictionaries.

    Args:
        blocks: List of dictionaries representing message content blocks

    Returns:
        Filtered list of non-empty text blocks
    """
    return [
        item
        for item in blocks
        if not (item.get("type") == "text" and not item.get("text", "").strip())
    ]

