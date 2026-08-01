
def _set_early_span_kind(span: "Span", kwargs: dict) -> None:
    """Defensively set OPENINFERENCE_SPAN_KIND before any other logic runs."""
    slp = kwargs.get("standard_logging_object")
    call_type = slp.get("call_type") if isinstance(slp, dict) else None
    safe_set_attribute(
        span,
        SpanAttributes.OPENINFERENCE_SPAN_KIND,
        _infer_open_inference_span_kind(call_type=call_type),
    )

