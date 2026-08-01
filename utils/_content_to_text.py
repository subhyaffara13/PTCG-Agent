
def _content_to_text(content: Any) -> str:
    """
    Convert OpenAI/Anthropic message content blocks to plain text.

    Text extraction policy:
    - Include text-bearing fields only (`text` blocks + string values).
    - For `tool_result`, expand into nested `content` items.
    - Ignore non-textual blocks (images/documents/tool metadata/thinking metadata).

    Implemented iteratively (stack-based) to avoid unbounded recursion.
    """
    parts: List[str] = []
    stack: List[Any] = [content]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            parts.append(item)
        elif isinstance(item, list):
            # Push list items in reverse order so they are processed left-to-right.
            for element in reversed(item):
                stack.append(element)
        elif isinstance(item, dict):
            item_type = item.get("type")
            if item_type == "text":
                parts.append(str(item.get("text", "")))
            elif item_type == "tool_result":
                stack.append(item.get("content", ""))
    return " ".join(parts)


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = [
            block.get("text")
            for block in content
            if isinstance(block, dict) and isinstance(block.get("text"), str)
        ]
        return " ".join(part for part in text_parts if part)
    return ""

