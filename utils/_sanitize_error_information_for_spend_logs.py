from typing import Optional

def _sanitize_error_information_for_spend_logs(
    error_information: Optional[StandardLoggingPayloadErrorInformation],
) -> Optional[StandardLoggingPayloadErrorInformation]:
    """
    Sanitize ``error_information`` before it lands in ``LiteLLM_SpendLogs.metadata``.

    Provider errors are stored verbatim via ``str(original_exception)``; those
    strings can echo the full request body, producing multi-megabyte spend-log
    rows.

    - Always: cap ``error_message`` and ``traceback`` with the existing
      ``MAX_STRING_LENGTH_PROMPT_IN_DB`` DB-storage safeguard.
    - When ``store_prompts_in_spend_logs`` is False: additionally redact
      ``'input'`` / ``'messages'`` / ``'prompt'`` values *and* Pydantic v2
      ``input_value=...`` assignments inside both ``error_message`` and
      ``traceback`` so prompts cannot leak through either field.

    Scoped to the spend-log path — OTEL/Datadog/etc. callbacks still receive
    the untruncated error per ``LITELLM_TRUNCATION_DB_SAFEGUARD_NOTE``.
    """
    if error_information is None:
        return None

    sanitized = cast(dict, {**error_information})

    if not _should_store_prompts_and_responses_in_spend_logs():
        for field in ("error_message", "traceback"):
            value = sanitized.get(field)
            if isinstance(value, str):
                sanitized[field] = _redact_prompt_leaks_in_error_string(value)

    sanitized = _sanitize_request_body_for_spend_logs_payload(sanitized)
    return cast(StandardLoggingPayloadErrorInformation, sanitized)

