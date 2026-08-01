
def truncate_base64_in_messages(
    messages: Optional[Union[str, list, dict]],
) -> Optional[Union[str, list, dict]]:
    """
    Return a copy of *messages* with long base64 data-URI payloads replaced
    by human-readable size placeholders.
    """
    if messages is None or MAX_BASE64_LENGTH_FOR_LOGGING <= 0:
        return messages
    try:
        return _truncate_base64_in_value(messages)
    except Exception as e:
        verbose_logger.debug("Failed to truncate base64 in messages: %s", e)
        return messages

