from typing import Optional

def _get_messages_for_spend_logs_payload(
    standard_logging_payload: Optional[StandardLoggingPayload],
    metadata: Optional[dict] = None,
) -> str:
    if _should_store_prompts_and_responses_in_spend_logs():
        if standard_logging_payload is not None:
            call_type = standard_logging_payload.get("call_type", "")
            if call_type == "_arealtime":
                messages = standard_logging_payload.get("messages")
                if messages is not None:
                    try:
                        return safe_dumps(messages)
                    except Exception:
                        return "{}"
    return "{}"

