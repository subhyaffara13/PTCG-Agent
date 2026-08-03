from typing import Any, Optional

def _get_response_for_spend_logs_payload(
    payload: Optional[StandardLoggingPayload],
    kwargs: Optional[dict] = None,
) -> str:
    if payload is None:
        return "{}"
    if _should_store_prompts_and_responses_in_spend_logs():
        response_obj: Any = payload.get("response")
        if response_obj is None:
            return "{}"

        if kwargs is not None:
            realtime_tool_calls = kwargs.get("realtime_tool_calls")
            if realtime_tool_calls and isinstance(response_obj, dict):
                response_obj = dict(response_obj)
                response_obj["tool_calls"] = realtime_tool_calls

        # Apply message redaction if turn_off_message_logging is enabled
        if kwargs is not None:
            from litellm.litellm_core_utils.redact_messages import (
                perform_redaction,
                should_redact_message_logging,
            )

            litellm_params = kwargs.get("litellm_params", {})
            model_call_details = {
                "litellm_params": litellm_params,
                "standard_callback_dynamic_params": kwargs.get(
                    "standard_callback_dynamic_params"
                ),
            }

            # If redaction is enabled, convert to serializable dict before redacting
            if should_redact_message_logging(model_call_details=model_call_details):
                response_obj = _convert_to_json_serializable_dict(response_obj)
                response_obj = perform_redaction(
                    model_call_details={}, result=response_obj
                )

        sanitized_wrapper = _sanitize_request_body_for_spend_logs_payload(
            {"response": response_obj}
        )

        sanitized_response = sanitized_wrapper.get("response", response_obj)

        if sanitized_response is None:
            return "{}"
        if isinstance(sanitized_response, str):
            result_str = strip_null_bytes(sanitized_response)
        else:
            result_str = safe_dumps(sanitized_response)
        if LITELLM_TRUNCATED_PAYLOAD_FIELD in result_str:
            verbose_proxy_logger.info(
                "Spend Log: response was truncated before storing in DB. %s",
                LITELLM_TRUNCATION_DB_SAFEGUARD_NOTE,
            )
        return result_str
    return "{}"

