
def _extract_text_from_responses_output(response: ResponsesAPIResponse) -> str:
    """Pull the assistant's text from the provider's response."""
    for item in response.output:
        item_type = (
            item.get("type") if isinstance(item, dict) else getattr(item, "type", None)
        )
        if item_type == "message":
            content = (
                item.get("content")
                if isinstance(item, dict)
                else getattr(item, "content", [])
            )
            for block in content or []:
                block_type = (
                    block.get("type")
                    if isinstance(block, dict)
                    else getattr(block, "type", None)
                )
                if block_type == "output_text":
                    raw = (
                        block.get("text")
                        if isinstance(block, dict)
                        else getattr(block, "text", "")
                    )
                    return str(raw) if raw is not None else ""
    return ""

