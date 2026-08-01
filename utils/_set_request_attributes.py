
def _set_request_attributes(
    span: "Span",
    kwargs,
    standard_logging_payload: StandardLoggingPayload,
    optional_params: dict,
    litellm_params: dict,
    response_obj,
    span_attrs,
):
    if kwargs.get("model"):
        safe_set_attribute(span, span_attrs.LLM_MODEL_NAME, kwargs.get("model"))

    safe_set_attribute(
        span, "llm.request.type", standard_logging_payload.get("call_type")
    )
    safe_set_attribute(
        span,
        span_attrs.LLM_PROVIDER,
        litellm_params.get("custom_llm_provider", "Unknown"),
    )

    if optional_params.get("max_tokens"):
        safe_set_attribute(
            span, "llm.request.max_tokens", optional_params.get("max_tokens")
        )
    if optional_params.get("temperature"):
        safe_set_attribute(
            span, "llm.request.temperature", optional_params.get("temperature")
        )
    if optional_params.get("top_p"):
        safe_set_attribute(span, "llm.request.top_p", optional_params.get("top_p"))

    safe_set_attribute(
        span, "llm.is_streaming", str(optional_params.get("stream", False))
    )

    if optional_params.get("user"):
        safe_set_attribute(span, "llm.user", optional_params.get("user"))

    if response_obj and response_obj.get("id"):
        safe_set_attribute(span, "llm.response.id", response_obj.get("id"))
    if response_obj and response_obj.get("model"):
        safe_set_attribute(span, "llm.response.model", response_obj.get("model"))

