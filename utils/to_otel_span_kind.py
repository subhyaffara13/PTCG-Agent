
def to_otel_span_kind(kind: LiteLLMSpanKind) -> SpanKind:
    return _SPAN_KIND_BY_ROLE_KIND[kind]

