
def _normalize_escaped_newlines(text: str) -> str:
    """
    Replace literal escaped newlines (backslash + n or backslash + r) with real newlines.
    API/JSON payloads sometimes deliver newlines as the two-character sequence \\n.

    Only applies when the text contains NO real newlines — this heuristic distinguishes
    JSON-escaped payloads (where all newlines are literal \\n) from normal text that
    may legitimately discuss escape sequences (e.g. "use \\n for newlines").
    """
    if not text:
        return text
    if "\\n" not in text and "\\r" not in text:
        return text
    # Only normalize when the text has no real newlines — this indicates
    # the entire payload came through with escaped newlines (e.g. from JSON).
    # If real newlines already exist, the text is already properly formatted
    # and literal \\n may be intentional content (e.g. discussing escape sequences).
    if "\n" in text or "\r" in text:
        return text
    # Order matters: replace \r\n first so we don't produce extra \n from \r then \n
    text = text.replace("\\r\\n", "\n")
    text = text.replace("\\n", "\n")
    text = text.replace("\\r", "\n")
    return text

