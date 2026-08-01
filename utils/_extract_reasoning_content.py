
def _extract_reasoning_content(message: dict) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract reasoning content and main content from a message.

    Args:
        message (dict): The message dictionary that may contain reasoning_content

    Returns:
        tuple[Optional[str], Optional[str]]: A tuple of (reasoning_content, content)
    """
    message_content = message.get("content")
    if "reasoning_content" in message:
        return message["reasoning_content"], message_content
    elif "reasoning" in message:
        return message["reasoning"], message_content
    elif isinstance(message_content, str):
        return _parse_content_for_reasoning(message_content)
    return None, message_content

