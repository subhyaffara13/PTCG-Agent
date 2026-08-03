from typing import Any, Optional

def get_active_span() -> Optional[Any]:
    """
    Return the active Datadog span, checking current span first and then root span.
    """
    try:
        current_span_fn = getattr(tracer, "current_span", None)
        if callable(current_span_fn):
            current_span = current_span_fn()
            if current_span is not None:
                return current_span

        current_root_span_fn = getattr(tracer, "current_root_span", None)
        if callable(current_root_span_fn):
            return current_root_span_fn()
    except Exception:
        return None
    return None

