
def get_metrics_context() -> MetricsContext:
    if not hasattr(_metrics_context_tls, "metrics_context"):
        _metrics_context_tls.metrics_context = MetricsContext(
            on_exit=record_compilation_metrics
        )
    return _metrics_context_tls.metrics_context

