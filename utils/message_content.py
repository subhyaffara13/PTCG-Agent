
def message_content(message: object) -> str | None:
    """Extract the textual ``content`` from a chat message dict."""
    if not isinstance(message, dict):
        return None
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        # multimodal: concatenate text parts only
        parts = [
            part.get("text", "")
            for part in content
            if isinstance(part, dict) and part.get("type") == "text"
        ]
        return "".join(p for p in parts if isinstance(p, str)) or None
    return None

