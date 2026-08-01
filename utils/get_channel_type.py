
def get_channel_type(channel: str | bytes) -> ChannelType | None:
    """
    Determine the type of a Redis keyspace notification channel.

    Args:
        channel: The channel name to check (string or bytes).

    Returns:
        ChannelType.KEYSPACE if it's a keyspace notification channel,
        ChannelType.KEYEVENT if it's a keyevent notification channel,
        None if it's not a keyspace notification channel.

    Examples:
        >>> get_channel_type("__keyspace@0__:mykey")
        ChannelType.KEYSPACE
        >>> get_channel_type("__keyevent@0__:set")
        ChannelType.KEYEVENT
        >>> get_channel_type("regular_channel") is None
        True
        >>> get_channel_type(b"__keyspace@0__:mykey")
        ChannelType.KEYSPACE
    """
    channel_str = safe_str(channel)
    # Check subkey prefixes first (they are longer and more specific)
    if channel_str.startswith(SubkeyspaceitemChannel.PREFIX):
        return ChannelType.SUBKEYSPACEITEM
    if channel_str.startswith(SubkeyspaceeventChannel.PREFIX):
        return ChannelType.SUBKEYSPACEEVENT
    if channel_str.startswith(SubkeyspaceChannel.PREFIX):
        return ChannelType.SUBKEYSPACE
    if channel_str.startswith(SubkeyeventChannel.PREFIX):
        return ChannelType.SUBKEYEVENT
    if channel_str.startswith(KeyspaceChannel.PREFIX):
        return ChannelType.KEYSPACE
    if channel_str.startswith(KeyeventChannel.PREFIX):
        return ChannelType.KEYEVENT
    return None

