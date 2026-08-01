
def _is_pattern(
    channel: str | bytes | KeyspaceChannel | KeyeventChannel,
) -> bool:
    """
    Check if a channel string contains glob-style pattern characters.

    Redis uses glob-style patterns for psubscribe:
    - * matches any sequence of characters
    - ? matches any single character
    - [...] matches any character in the brackets

    Args:
        channel: The channel string to check. Can be a string, bytes,
                 or a KeyspaceChannel/KeyeventChannel object.

    Returns:
        True if the channel contains pattern characters, False otherwise.
    """
    # Handle Channel objects that have _channel_str attribute
    # (KeyspaceChannel, KeyeventChannel)
    if hasattr(channel, "_channel_str"):
        channel = channel._channel_str
    channel = safe_str(channel)
    # Check for unescaped glob pattern characters.
    # * and ? are always pattern characters.
    # [ is only a pattern character when followed by a matching unescaped ],
    # forming a bracket expression like [abc] or [a-z].  A lone [ (e.g. in
    # a key named "my[key") is treated as a literal by Redis.
    i = 0
    while i < len(channel):
        char = channel[i]
        if char == "\\":
            # Skip escaped character
            i += 2
            continue
        if char in ("*", "?"):
            return True
        if char == "[":
            # Look for a matching unescaped ]
            j = i + 1
            while j < len(channel):
                if channel[j] == "\\":
                    j += 2
                    continue
                if channel[j] == "]":
                    return True
                j += 1
            # No matching ] found — literal [
        i += 1
    return False

