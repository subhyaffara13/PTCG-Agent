
def is_text_content_call_type(call_type: str) -> bool:
    """Return True if ``call_type`` carries free-form text that text
    guardrails should inspect (Chat Completions or Responses API)."""
    return call_type in TEXT_CONTENT_CALL_TYPES

