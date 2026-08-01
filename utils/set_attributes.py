
def set_attributes(
    span: "Span", kwargs, response_obj, attributes: Type[BaseLLMObsOTELAttributes]
):
    """
    Populates span with OpenInference-compliant LLM attributes for Arize and Phoenix tracing.
    """
    # Coerce non-dict response objects (e.g. httpx.Response from passthrough
    # routes) into a dict so downstream `.get()` calls don't crash. Existing
    # dict / `.get()`-bearing objects (incl. Pydantic OpenAI Responses API
    # models) are returned unchanged, preserving the existing test behavior.
    response_obj_for_attrs = _coerce_response_obj_for_attrs(response_obj)

    # Set span.kind defensively before anything else. If a downstream step
    # throws, the span still has a kind so Arize can render it correctly
    # (an LLM call instead of UNKNOWN). This is the single source of truth
    # for span.kind — no late re-write happens below.
    _safe_emit("early span kind", _set_early_span_kind, span, kwargs)

    try:
        optional_params = _sanitize_optional_params(kwargs.get("optional_params"))
        litellm_params = kwargs.get("litellm_params", {}) or {}
        standard_logging_payload: Optional[StandardLoggingPayload] = kwargs.get(
            "standard_logging_object"
        )
        if standard_logging_payload is None:
            raise ValueError("standard_logging_object not found in kwargs")

        metadata = (
            standard_logging_payload.get("metadata")
            if standard_logging_payload
            else None
        )
        _set_metadata_attributes(span, metadata, SpanAttributes)

        metadata_tools = _extract_metadata_tools(metadata)
        optional_tools = _extract_optional_tools(optional_params)

        _set_request_attributes(
            span=span,
            kwargs=kwargs,
            standard_logging_payload=standard_logging_payload,
            optional_params=optional_params,
            litellm_params=litellm_params,
            response_obj=response_obj_for_attrs,
            span_attrs=SpanAttributes,
        )

        # span.kind was already set above by `_set_early_span_kind`. We do
        # NOT re-write it here based on tool presence: a chat completion
        # that passes `tools=[...]` (or returns `tool_calls`) is still an
        # LLM call per the OpenInference spec — TOOL is reserved for actual
        # tool execution spans, not LLM calls that request tools.
        _set_tool_attributes(span, optional_tools, metadata_tools)
        attributes.set_messages(span, kwargs)

        model_params = (
            standard_logging_payload.get("model_parameters")
            if standard_logging_payload
            else None
        )
        _set_model_params(span, model_params, SpanAttributes)

        _set_response_attributes(span=span, response_obj=response_obj_for_attrs)

    except Exception as e:
        verbose_logger.error(
            f"[Arize/Phoenix] Failed to set OpenInference span attributes: {e}"
        )
        if hasattr(span, "record_exception"):
            span.record_exception(e)

    # Additive emitters. Each is independently guarded so a failure can never
    # blank the attributes set by the main try-block above. New attributes are
    # written under new keys; existing attributes are not overwritten.
    slp = kwargs.get("standard_logging_object")
    _safe_emit("session/user attrs", _set_session_and_user_attrs, span, kwargs, slp)
    _safe_emit("response cost", _set_response_cost_attr, span, slp)
    _safe_emit(
        "passthrough normalization",
        _maybe_normalize_passthrough,
        span,
        kwargs,
        response_obj,
        response_obj_for_attrs,
        slp,
    )

