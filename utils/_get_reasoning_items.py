
def _get_reasoning_items(
    msg: "AllMessageValues",
) -> List[ChatCompletionReasoningItem]:
    """Extract reasoning_items from a message dict with proper typing."""
    items = msg.get("reasoning_items")  # type: ignore[union-attr]
    if items:
        return items  # type: ignore[return-value]
    return []

