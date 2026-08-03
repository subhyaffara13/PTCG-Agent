from typing import Optional

def record_streaming_lag(
    lag_seconds: float,
    stream_name: Optional[str] = None,
    consumer_group: Optional[str] = None,
    consumer_name: Optional[str] = None,  # noqa
) -> None:
    """
    Record the lag of a streaming message.

    Args:
        lag_seconds: Lag in seconds
        stream_name: Stream name
        consumer_group: Consumer group name
        consumer_name: Consumer name
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    # Check if stream names should be hidden
    effective_stream_name = stream_name
    if stream_name is not None:
        config = _get_config()
        if config is not None and config.hide_stream_names:
            effective_stream_name = None

    try:
        _metrics_collector.record_streaming_lag(
            lag_seconds=lag_seconds,
            stream_name=effective_stream_name,
            consumer_group=consumer_group,
        )
    except Exception:
        pass

