from typing import Optional

def _get_prometheus_logger_from_callbacks() -> Optional[PrometheusLogger]:
    """
    Checks if prometheus is a initalized callback, if yes returns it
    """
    from litellm.integrations.prometheus import PrometheusLogger

    if PrometheusLogger is None:
        return None

    for _callback in litellm._async_success_callback:
        if isinstance(_callback, PrometheusLogger):
            return _callback
    for global_callback in litellm.callbacks:
        if isinstance(global_callback, PrometheusLogger):
            return global_callback

    return None

