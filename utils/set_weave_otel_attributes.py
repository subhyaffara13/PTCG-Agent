from typing import Any

def set_weave_otel_attributes(span: Span, kwargs: dict[str, Any], response_obj: Any):
    """
    Sets OpenTelemetry span attributes for Weave observability.
    Uses the same attribute setting logic as other OTEL integrations for consistency.
    """
    _utils.set_attributes(span, kwargs, response_obj, WeaveLLMObsOTELAttributes)
    _set_weave_specific_attributes(span=span, kwargs=kwargs, response_obj=response_obj)

