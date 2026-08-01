
def _redact_standard_logging_object(model_call_details: dict):
    """Redact messages and response inside standard_logging_object if present."""
    standard_logging_object = model_call_details.get("standard_logging_object")
    if standard_logging_object is None:
        return

    redacted_str = "redacted-by-litellm"

    if standard_logging_object.get("messages") is not None:
        standard_logging_object["messages"] = [
            {"role": "user", "content": redacted_str}
        ]

    response = standard_logging_object.get("response")
    if response is not None:
        if isinstance(response, dict) and "output" in response:
            # ResponsesAPIResponse format - redact content in output items
            if isinstance(response.get("output"), list):
                _redact_responses_api_output_dict(response["output"], redacted_str)
            redact_vertex_ai_metadata_from_logged_object(response)
        elif isinstance(response, dict) and "choices" in response:
            # ModelResponse dict format - redact content in choices
            if isinstance(response.get("choices"), list):
                _redact_model_response_dict_choices(response["choices"], redacted_str)
            redact_vertex_ai_metadata_from_logged_object(response)
        elif isinstance(response, str):
            standard_logging_object["response"] = redacted_str
        else:
            # For other formats (empty dict, None, etc.), use simple text format
            standard_logging_object["response"] = {"text": redacted_str}

