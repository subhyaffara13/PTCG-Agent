from typing import Any, Dict, List

def extract_text_from_a2a_message(message: Any) -> str:
    return A2ARequestUtils.extract_text_from_message(message)


def extract_text_from_a2a_message(
    message: Dict[str, Any], depth: int = 0, max_depth: int = 10
) -> str:
    """
    Extract text content from A2A message parts.

    Args:
        message: A2A message dict with 'parts' containing text parts
        depth: Current recursion depth (internal use)
        max_depth: Maximum recursion depth to prevent infinite loops

    Returns:
        Concatenated text from all text parts
    """
    if message is None or depth >= max_depth:
        return ""

    parts = message.get("parts", [])
    text_parts: List[str] = []

    for part in parts:
        if part.get("kind") == "text":
            text_parts.append(part.get("text", ""))
        # Handle nested parts if they exist
        elif "parts" in part:
            nested_text = extract_text_from_a2a_message(part, depth + 1, max_depth)
            if nested_text:
                text_parts.append(nested_text)

    return " ".join(text_parts)

