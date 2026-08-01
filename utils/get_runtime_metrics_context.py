
def get_runtime_metrics_context() -> RuntimeMetricsContext:
    if not hasattr(_metrics_context_tls, "runtime_metrics_context"):
        _metrics_context_tls.runtime_metrics_context = RuntimeMetricsContext(
            on_exit=record_compilation_metrics
        )
    return _metrics_context_tls.runtime_metrics_context

