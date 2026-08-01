
def _extract_response_text(response: Any) -> str:
    """Extract text from every LLM response choice."""
    if hasattr(response, "choices") and response.choices:
        text_parts: List[str] = []
        for choice in response.choices:
            if hasattr(choice, "message") and choice.message:
                text = _content_to_text(choice.message.content)
                if text:
                    text_parts.append(text)
        return "\n".join(text_parts)
    return ""


def _extract_response_text(response: Any) -> str:
    """Extract concatenated text from all text blocks in a response."""
    content = response.get("content") if isinstance(response, dict) else []
    if not isinstance(content, list):
        return ""
    parts = [
        b.get("text", "")
        for b in content
        if isinstance(b, dict) and b.get("type") == "text"
    ]
    return "\n".join(parts).strip()


def _extract_response_text(response: Any) -> Optional[str]:
    try:
        choice = response.choices[0]
        message = choice.message
        content = getattr(message, "content", None)
        if isinstance(content, str):
            return content
        # Some providers return a list of content parts.
        if isinstance(content, list):
            text_parts = [
                part.get("text", "")
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            ]
            return "".join(text_parts) or None
    except (AttributeError, IndexError, KeyError):
        return None
    return None

