from typing import Any

def _passthrough_span_name_hook(span: Any, scope: dict) -> None:
    """FastAPI ``server_request_hook``: give passthrough server spans a useful name.

    The instrumentation matches the route at span creation, so both the span name
    and ``http.route`` are set to the catch-all template (``/openai/{endpoint:path}``)
    before this hook runs. Rewrite both to the real request path so each upstream
    endpoint is distinguishable. (The ASGI ``http receive``/``http send`` sub-spans
    can't be renamed from here — their name is captured at creation — so they are
    dropped via ``exclude_spans`` at instrumentation time.)
    """
    try:
        if span is None or not span.is_recording():
            return
        path = scope.get("path") or ""
        method = scope.get("method") or ""
        first_segment = path.lstrip("/").split("/", 1)[0]
        if first_segment in PASSTHROUGH_PREFIXES:
            span.update_name(f"{method} {path}".strip())
            span.set_attribute("http.route", path)
    except Exception:
        pass

