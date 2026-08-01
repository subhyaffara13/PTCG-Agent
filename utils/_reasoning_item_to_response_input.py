
def _reasoning_item_to_response_input(
    r_item: Union[ChatCompletionReasoningItem, Dict[str, Any]],
) -> Dict[str, Any]:
    """Convert a stored ChatCompletionReasoningItem back to a Responses API input item."""
    r_input: Dict[str, Any] = {
        "type": "reasoning",
        "id": r_item.get("id") or f"rs_{id(r_item)}",
        # summary is always required by the Responses API, even when empty
        "summary": r_item.get("summary") or [],
    }
    if r_item.get("encrypted_content"):
        r_input["encrypted_content"] = r_item["encrypted_content"]
    return r_input

