
def _has_non_text_content(message: AllMessageValues) -> bool:
    """Check if a message has non-text content items (e.g. image_url)."""
    content = message.get("content")
    if not isinstance(content, list):
        return False
    return any(item.get("type") != "text" for item in content)

