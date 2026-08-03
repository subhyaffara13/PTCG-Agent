from typing import Optional

def _get_proxy_server_request_for_spend_logs_payload(
    metadata: dict,
    litellm_params: dict,
    kwargs: Optional[dict] = None,
) -> str:
    """
    Only store if _should_store_prompts_and_responses_in_spend_logs() is True

    If turn_off_message_logging is enabled, redact messages in the request body.
    """
    if _should_store_prompts_and_responses_in_spend_logs():
        _proxy_server_request = cast(
            Optional[dict], litellm_params.get("proxy_server_request", {})
        )
        if _proxy_server_request is not None:
            _request_body = _proxy_server_request.get("body", {}) or {}

            if kwargs is not None:
                realtime_tools = kwargs.get("realtime_tools")
                if realtime_tools:
                    _request_body = dict(_request_body)
                    _request_body["tools"] = realtime_tools

            # Apply message redaction if turn_off_message_logging is enabled
            if kwargs is not None:
                from litellm.litellm_core_utils.redact_messages import (
                    perform_redaction,
                    should_redact_message_logging,
                )

                # Build model_call_details dict to check redaction settings
                model_call_details = {
                    "litellm_params": litellm_params,
                    "standard_callback_dynamic_params": kwargs.get(
                        "standard_callback_dynamic_params"
                    ),
                }

                # If redaction is enabled, convert to serializable dict before redacting
                if should_redact_message_logging(model_call_details=model_call_details):
                    _request_body = _convert_to_json_serializable_dict(_request_body)
                    perform_redaction(model_call_details=_request_body, result=None)

            _request_body = _sanitize_request_body_for_spend_logs_payload(_request_body)
            _request_body_json_str = safe_dumps(_request_body)
            if LITELLM_TRUNCATED_PAYLOAD_FIELD in _request_body_json_str:
                verbose_proxy_logger.info(
                    "Spend Log: request body was truncated before storing in DB. %s",
                    LITELLM_TRUNCATION_DB_SAFEGUARD_NOTE,
                )
            return _request_body_json_str
    return "{}"

