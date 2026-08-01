
def redact_secrets(value: str) -> str:
    """Public API: redact known secret/credential patterns from an arbitrary string.

    Use this for code paths that bypass the logging system — e.g. Slack/Teams
    alerting, HTTP error response bodies, or any other string that may contain
    secrets and will be sent to an external sink.

    Not to be confused with redact_message_input_output_from_logging() in
    litellm_core_utils/redact_messages.py, which redacts LLM prompt/response
    content for privacy — this function redacts credential patterns (API keys,
    PEM blocks, tokens, etc.) by shape.
    """
    if not _ENABLE_SECRET_REDACTION:
        return value
    return _redact_string(value)

