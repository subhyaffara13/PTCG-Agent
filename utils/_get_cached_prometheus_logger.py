
def _get_cached_prometheus_logger():
    """
    Get cached PrometheusLogger class.
    Lazy imports on first call to avoid loading prometheus.py and utils.py at import time (60MB saved).
    Subsequent calls use cached class for better performance.
    """
    global _PrometheusLogger
    if _PrometheusLogger is None:
        from litellm.integrations.prometheus import PrometheusLogger

        _PrometheusLogger = PrometheusLogger
    return _PrometheusLogger

