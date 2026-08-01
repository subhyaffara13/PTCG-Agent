
def _ensure_parent_otel_span_on_request_state(request: Request) -> None:
    """Idempotently create the OTEL SERVER span and stash it on
    ``request.state.parent_otel_span``. Safe to call multiple times.

    Called both at the top of ``user_api_key_auth`` (so body-parse failures
    have a span to close) and inside ``_user_api_key_auth_builder`` (for
    callers that bypass ``user_api_key_auth``, e.g. MCP).
    """
    from litellm.proxy.proxy_server import open_telemetry_logger

    if open_telemetry_logger is None:
        return
    if getattr(request.state, "parent_otel_span", None) is not None:
        return
    start_time = datetime.now()
    try:
        request.state.litellm_received_at = start_time
    except Exception:
        pass
    parent_otel_span = open_telemetry_logger.create_litellm_proxy_request_started_span(
        start_time=start_time,
        headers=_safe_get_request_headers(request),
    )
    # Under V2 the FastAPI instrumentor stamps http.route / url.path on the server
    # span; only the legacy logger needs these set explicitly.
    set_route_attrs = getattr(
        open_telemetry_logger, "set_proxy_request_route_attributes", None
    )
    if not is_otel_v2_enabled() and set_route_attrs is not None:
        set_route_attrs(
            parent_otel_span,
            url_path=get_request_route(request=request),
            http_route=get_request_route_template(request),
        )
    request.state.parent_otel_span = parent_otel_span

