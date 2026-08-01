
def _sanitize_empty_content(message_dict: dict[str, Any]) -> None:
    """
    Remove or filter content so empty text blocks are not sent.
    Databricks Model Serving uses Anthropic Messages API spec and rejects empty text blocks.
    """
    content = message_dict.get("content")
    if content is None:
        message_dict.pop("content", None)
        return
    if isinstance(content, str):
        if not content.strip():
            message_dict.pop("content")
        return
    if isinstance(content, list):
        if not content:
            message_dict.pop("content")
            return
        filtered = [
            block
            for block in content
            if not (
                isinstance(block, dict)
                and block.get("type") == "text"
                and not (block.get("text") or "").strip()
            )
        ]
        if not filtered:
            message_dict.pop("content")
        else:
            message_dict["content"] = filtered

