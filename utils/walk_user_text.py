from typing import Any, Callable, Dict, List

def walk_user_text(data: Dict[str, Any], visit: Callable[[str], str]) -> int:
    """Rewrite every text fragment in place via ``visit``.

    Mutates ``data["messages"]`` and ``data["input"]``. Returns the number
    of fragments visited so callers can short-circuit when nothing was
    inspected.
    """
    visited = 0

    def _rewrite_content(content: Any) -> Any:
        nonlocal visited
        if isinstance(content, str):
            if content:
                visited += 1
                return visit(content)
            return content
        if isinstance(content, list):
            new_parts: List[Any] = []
            for part in content:
                if isinstance(part, str) and part:
                    visited += 1
                    new_parts.append(visit(part))
                elif (
                    isinstance(part, dict)
                    and part.get("type") == "text"
                    and isinstance(part.get("text"), str)
                    and part["text"]
                ):
                    visited += 1
                    new_parts.append({**part, "text": visit(part["text"])})
                else:
                    new_parts.append(part)
            return new_parts
        return content

    messages = data.get("messages")
    if isinstance(messages, list):
        for message in messages:
            if isinstance(message, dict) and "content" in message:
                message["content"] = _rewrite_content(message["content"])

    input_value = data.get("input")
    if isinstance(input_value, str):
        if input_value:
            visited += 1
            data["input"] = visit(input_value)
        return visited
    if isinstance(input_value, list):
        # List of full messages: rewrite each message's content.
        if input_value and all(
            isinstance(item, dict) and "role" in item for item in input_value
        ):
            for item in input_value:
                if "content" in item:
                    item["content"] = _rewrite_content(item["content"])
            return visited
        # List of content parts and/or bare strings: rewrite in place.
        for idx, item in enumerate(input_value):
            if isinstance(item, str) and item:
                visited += 1
                input_value[idx] = visit(item)
            elif (
                isinstance(item, dict)
                and item.get("type") == "text"
                and isinstance(item.get("text"), str)
                and item["text"]
            ):
                visited += 1
                input_value[idx] = {**item, "text": visit(item["text"])}
        return visited

    return visited

