
def is_anthropic_invalid_thinking_signature_error(error_text: str) -> bool:
    """
    Detect Anthropic 400 when encrypted thinking signatures in history do not match
    the current deployment (e.g. user rotated API key or switched model endpoint).

    Example API message:
    messages.N.content.M: Invalid `signature` in `thinking` block
    """
    if not error_text:
        return False
    lower = error_text.lower()
    return (
        "invalid" in lower
        and "signature" in lower
        and "thinking" in lower
        and "block" in lower
    )

