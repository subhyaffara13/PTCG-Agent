
def request_root_span() -> "Span | None":
    """The anchored request root span, or ``None`` outside a proxy request."""
    span = _request_root_span.get()
    return span if is_recordable_span(span) else None

