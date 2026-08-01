
def extract_ttl_from_cached_messages(messages: List[AllMessageValues]) -> Optional[str]:
    """
    Extract TTL from cached messages. Returns the first valid TTL found.

    Args:
        messages: List of messages to extract TTL from

    Returns:
        Optional[str]: TTL string in format "3600s" or None if not found/invalid
    """
    for message in messages:
        if not is_cached_message(message):
            continue

        content = message.get("content")
        if not content or isinstance(content, str):
            continue

        for content_item in content:
            # Type check to ensure content_item is a dictionary before calling .get()
            if not isinstance(content_item, dict):
                continue

            cache_control = content_item.get("cache_control")
            if not cache_control or not isinstance(cache_control, dict):
                continue

            if cache_control.get("type") != "ephemeral":
                continue

            ttl = cache_control.get("ttl")
            if ttl and _is_valid_ttl_format(ttl):
                return str(ttl)

    return None

