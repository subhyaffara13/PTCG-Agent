from typing import Any

def _append_text_to_content(content: Any, extra_text: str) -> Any:
    """Append ``extra_text`` to an OpenAI-shape message ``content`` field.

    Handles the two common shapes: ``str`` and ``list`` of content parts.
    For unexpected/empty shapes, fall back so the caller gets a usable value.
    """
    if content is None or content == "":
        return extra_text
    if isinstance(content, str):
        return f"{content}\n\n{extra_text}"
    if isinstance(content, list):
        return [*content, {"type": "text", "text": extra_text}]
    return [content, {"type": "text", "text": extra_text}]

