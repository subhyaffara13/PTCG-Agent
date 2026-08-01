
def classify_prompt(text: str) -> RequestType:
    """
    Classify a single user prompt.

    Falls back to GENERAL when no rule matches. Empty/whitespace-only also
    returns GENERAL.
    """
    if not text or not text.strip():
        return RequestType.GENERAL

    truncated = text[:2000]

    for pattern, request_type in _RULES:
        if pattern.search(truncated):
            return request_type

    return RequestType.GENERAL

