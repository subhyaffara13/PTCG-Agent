
def is_cached_message(message: AllMessageValues) -> bool:
    """
    Returns true, if message is marked as needing to be cached.

    Used for anthropic/gemini context caching.

    Follows the anthropic format {"cache_control": {"type": "ephemeral"}}

    Can be disabled globally by setting litellm.disable_anthropic_gemini_context_caching_transform = True
    """
    # Check if context caching is disabled globally
    if litellm.disable_anthropic_gemini_context_caching_transform is True:
        return False

    # Check message-level cache_control (set by cache_control_injection_points hook for string content)
    message_level_cache_control = message.get("cache_control")
    if (
        message_level_cache_control is not None
        and isinstance(message_level_cache_control, dict)
        and message_level_cache_control.get("type") == "ephemeral"
    ):
        return True

    if "content" not in message:
        return False

    content = message["content"]

    # Handle non-list content types (None, str, etc.)
    if not isinstance(content, list):
        return False

    for content_item in content:
        # Ensure content_item is a dictionary before accessing keys
        if not isinstance(content_item, dict):
            continue

        cache_control = content_item.get("cache_control")
        if (
            content_item.get("type") == "text"
            and cache_control is not None
            and isinstance(cache_control, dict)
            and cache_control.get("type") == "ephemeral"
        ):
            return True

    return False

