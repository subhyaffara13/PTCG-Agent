from typing import Optional

def _close_dangling_otel_server_span(
    request: Request, status_code: int, exc: Optional[Exception] = None
) -> None:
    parent_otel_span = getattr(request.state, "parent_otel_span", None)
    if parent_otel_span is None:
        return
    if open_telemetry_logger is None:
        return
    # Under OTel V2 the FastAPI instrumentor owns the server span (parent_otel_span
    # is that same span), and it records the error + ends it itself. Ending it here
    # would end it early — losing the http.* attributes the instrumentor stamps on
    # completion — and double-end it. Leave it to the instrumentor.
    try:
        from litellm.integrations.otel.model.config import is_otel_v2_enabled

        if is_otel_v2_enabled():
            return
    except Exception:
        pass
    try:
        from opentelemetry.trace import Status, StatusCode

        open_telemetry_logger.set_response_status_code_attribute(
            parent_otel_span, status_code
        )
        if status_code >= 400:
            open_telemetry_logger.record_error_attributes_on_span(
                parent_otel_span, exc, status_code
            )
        parent_otel_span.set_status(
            Status(StatusCode.ERROR if status_code >= 400 else StatusCode.OK)
        )
        parent_otel_span.end()
    except Exception as e:
        verbose_proxy_logger.debug(
            "Error closing dangling OTEL SERVER span: %s", str(e)
        )
    finally:
        request.state.parent_otel_span = None

