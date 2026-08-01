
def record_output_item_chunk(
    parsed_chunk: Dict[str, Any],
    output_items: Dict[int, Dict[str, Any]],
) -> None:
    """Record an OUTPUT_ITEM_DONE chunk into ``output_items`` keyed by
    ``output_index`` (falling back to the next free slot when missing).
    """
    item = parsed_chunk.get("item")
    if not isinstance(item, dict):
        return
    try:
        output_index_raw = parsed_chunk.get("output_index")
        if output_index_raw is None:
            raise ValueError("missing output_index")
        output_index = int(output_index_raw)
    except (TypeError, ValueError):
        output_index = len(output_items)
    output_items[output_index] = item

