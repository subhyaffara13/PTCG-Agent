from typing import Optional

def _coerce_text(value) -> Optional[str]:
    """Best-effort text extraction from a message-content value.

    Returns None when no textual portion can be derived. Handles:
      - plain strings
      - lists of OpenAI-style content parts (`{"type": "text", "text": ...}`)
      - lists of Anthropic-style content parts (`{"type": "text", "text": ...}`
        or `{"type": "input_text", "text": ...}`)
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for part in value:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                text = part.get("text") or part.get("input_text")
                if isinstance(text, str):
                    parts.append(text)
        if parts:
            return "\n".join(parts)
    return None

