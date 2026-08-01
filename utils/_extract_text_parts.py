
def _extract_text_parts(content: Any) -> Optional[str]:
    """Extract text parts from mixed content."""
    items = content if isinstance(content, list) else [content]
    texts = []
    for item in items:
        if getattr(item, "type", None) == "text":
            texts.append(getattr(item, "text", ""))
    return "\n".join(texts) if texts else None

