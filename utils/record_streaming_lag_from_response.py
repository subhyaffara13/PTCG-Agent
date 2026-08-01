
def record_streaming_lag_from_response(
    response,
    consumer_group: Optional[str] = None,
    consumer_name: Optional[str] = None,  # noqa
) -> None:
    """
    Record streaming lag from XREAD/XREADGROUP response.

    Parses the response and calculates lag for each message based on message ID timestamp.

    Args:
        response: Response from XREAD/XREADGROUP command
        consumer_group: Consumer group name (for XREADGROUP)
        consumer_name: Consumer name (for XREADGROUP)
    """

    global _metrics_collector

    if _metrics_collector is None:
        _metrics_collector = _get_or_create_collector()
        if _metrics_collector is None:
            return

    if not response:
        return

    try:
        now = datetime.now().timestamp()

        # Check if stream names should be hidden
        config = _get_config()
        hide_stream_names = config is not None and config.hide_stream_names

        # RESP3 format: dict
        if isinstance(response, dict):
            for stream_name, stream_messages in response.items():
                effective_stream_name = (
                    None if hide_stream_names else str_if_bytes(stream_name)
                )
                for messages in stream_messages:
                    for message in messages:
                        message_id, _ = message
                        message_id = str_if_bytes(message_id)
                        timestamp, _ = message_id.split("-")
                        # Ensure lag is non-negative (clock skew can cause negative values)
                        lag_seconds = max(0.0, now - int(timestamp) / 1000)

                        _metrics_collector.record_streaming_lag(
                            lag_seconds=lag_seconds,
                            stream_name=effective_stream_name,
                            consumer_group=consumer_group,
                        )
        else:
            # RESP2 format: list
            for stream_entry in response:
                stream_name = str_if_bytes(stream_entry[0])
                effective_stream_name = None if hide_stream_names else stream_name

                for message in stream_entry[1]:
                    message_id, _ = message
                    message_id = str_if_bytes(message_id)
                    timestamp, _ = message_id.split("-")
                    # Ensure lag is non-negative (clock skew can cause negative values)
                    lag_seconds = max(0.0, now - int(timestamp) / 1000)

                    _metrics_collector.record_streaming_lag(
                        lag_seconds=lag_seconds,
                        stream_name=effective_stream_name,
                        consumer_group=consumer_group,
                    )
    except Exception:
        pass

