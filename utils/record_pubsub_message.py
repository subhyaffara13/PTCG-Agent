
def record_pubsub_message(
    direction: PubSubDirection,
    channel: Optional[str] = None,
    sharded: Optional[bool] = None,
) -> None:
    """
    Record a PubSub message (published or received).

    Args:
        direction: Message direction ('publish' or 'receive')
        channel: Pub/Sub channel name
        sharded: True if sharded Pub/Sub channel

    Example:
        >>> record_pubsub_message(PubSubDirection.PUBLISH, 'channel', False)
    """
    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    # Check if channel names should be hidden
    effective_channel = channel
    if channel is not None:
        config = _get_config()
        if config is not None and config.hide_pubsub_channel_names:
            effective_channel = None

    try:
        _metrics_collector.record_pubsub_message(
            direction=direction,
            channel=effective_channel,
            sharded=sharded,
        )
    except Exception:
        pass

