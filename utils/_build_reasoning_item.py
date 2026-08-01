
def _build_reasoning_item(
    item_id: str,
    encrypted_content: Optional[str],
    summary_raw: Any,
) -> Dict[str, Any]:
    """Build a ChatCompletionReasoningItem-shaped dict from raw response data.

    Handles both pydantic objects (attribute access) and plain dicts.
    """
    summary: List[Dict[str, Any]] = []
    for s in summary_raw or []:
        if isinstance(s, dict):
            summary.append(
                {"type": s.get("type", "summary_text"), "text": s.get("text", "")}
            )
        else:
            summary.append(
                {
                    "type": getattr(s, "type", "summary_text"),
                    "text": getattr(s, "text", ""),
                }
            )
    return {
        "id": item_id,
        "type": "reasoning",
        "encrypted_content": encrypted_content,
        "summary": summary,
    }

