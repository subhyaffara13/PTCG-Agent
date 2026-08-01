
def perform_redaction(model_call_details: dict, result):
    """
    Performs the actual redaction on the logging object and result.
    """
    # Redact model_call_details
    model_call_details["messages"] = [
        {"role": "user", "content": "redacted-by-litellm"}
    ]
    model_call_details["prompt"] = ""
    model_call_details["input"] = ""
    _redact_standard_logging_object(model_call_details)
    redact_vertex_ai_metadata_from_litellm_params(model_call_details)

    # Redact streaming response
    if (
        model_call_details.get("stream", False) is True
        and "complete_streaming_response" in model_call_details
    ):
        _streaming_response = model_call_details["complete_streaming_response"]
        if hasattr(_streaming_response, "choices"):
            for choice in _streaming_response.choices:
                _redact_choice_content(choice)
            redact_vertex_ai_metadata_from_logged_object(_streaming_response)
        elif hasattr(_streaming_response, "output"):
            _redact_responses_api_output(_streaming_response.output)
            # Redact reasoning field in ResponsesAPIResponse
            if (
                hasattr(_streaming_response, "reasoning")
                and _streaming_response.reasoning is not None
            ):
                _streaming_response.reasoning = None

    # Redact result
    if result is not None:
        # Check if result is a coroutine, async generator, or other async object - these cannot be deepcopied
        if (
            asyncio.iscoroutine(result)
            or inspect.iscoroutinefunction(result)
            or hasattr(result, "__aiter__")
            or hasattr(result, "__anext__")  # async generator
        ):  # async iterator
            # For async objects, return a simple redacted response without deepcopy
            return {"text": "redacted-by-litellm"}

        _result = copy.deepcopy(result)
        if isinstance(_result, litellm.ModelResponse):
            if hasattr(_result, "choices") and _result.choices is not None:
                for choice in _result.choices:
                    _redact_choice_content(choice)
            redact_vertex_ai_metadata_from_logged_object(_result)
        elif isinstance(_result, dict) and "choices" in _result:
            # Handle dict representation of ModelResponse (e.g., from model_dump())
            if _result.get("choices") is not None:
                _redact_model_response_dict_choices(
                    _result["choices"], "redacted-by-litellm"
                )
            redact_vertex_ai_metadata_from_logged_object(_result)
        elif isinstance(_result, dict) and "output" in _result:
            if isinstance(_result.get("output"), list):
                _redact_responses_api_output_dict(
                    _result["output"], "redacted-by-litellm"
                )
        elif isinstance(_result, litellm.ResponsesAPIResponse):
            if hasattr(_result, "output"):
                _redact_responses_api_output(_result.output)
            # Redact reasoning field in ResponsesAPIResponse
            if hasattr(_result, "reasoning") and _result.reasoning is not None:
                _result.reasoning = None
        elif isinstance(_result, litellm.EmbeddingResponse):
            if hasattr(_result, "data") and _result.data is not None:
                _result.data = []
        else:
            return {"text": "redacted-by-litellm"}
        return _result

