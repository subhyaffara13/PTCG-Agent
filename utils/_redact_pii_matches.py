
def _redact_pii_matches(response_json: dict) -> dict:
    """
    Redact match-like fields from a Bedrock ApplyGuardrail JSON payload.

    Delegates to :func:`redact_nested_match_and_regex_keys` (same rules as spend
    logging). Kept as a Bedrock-module entry point for existing unit tests.
    """
    redacted = redact_nested_match_and_regex_keys(response_json)
    return redacted if isinstance(redacted, dict) else response_json

