
def span_role_for_service(service_name: str) -> SpanRole | None:
    """The span role for a service call, or ``None`` when it must not be a span.

    ``DB_CALL`` for outbound datastores, ``SERVICE`` for genuine internal work
    worth a span (background jobs), and ``None`` for framework instrumentation
    that duplicates a gen-AI span or belongs in metrics only
    (see ``_METRICS_ONLY_SERVICES``).
    """
    if service_name in _METRICS_ONLY_SERVICES:
        return None
    return SpanRole.DB_CALL if db_system(service_name) is not None else SpanRole.SERVICE

