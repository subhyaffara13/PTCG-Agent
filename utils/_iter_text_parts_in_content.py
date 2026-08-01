
def _iter_text_parts_in_content(content: Any) -> Iterator[str]:
    """Yield text fragments from a ``message.content`` value (string or
    multimodal list). Non-text parts (images, audio, …) are skipped."""
    if isinstance(content, str):
        if content:
            yield content
    elif isinstance(content, list):
        for part in content:
            if isinstance(part, str):
                # A bare string in a content/input list is itself a text
                # fragment (Responses-API mixed-list shape).
                if part:
                    yield part
                continue
            if not isinstance(part, dict):
                continue
            if part.get("type") == "text":
                text = part.get("text")
                if isinstance(text, str) and text:
                    yield text

