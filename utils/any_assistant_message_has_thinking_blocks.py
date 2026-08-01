
def any_assistant_message_has_thinking_blocks(
    messages: List[AllMessageValues],
) -> bool:
    """
    Returns true if ANY assistant message has thinking_blocks.

    This is used to prevent dropping the thinking param when some messages
    in the conversation already contain thinking blocks. Dropping thinking
    when thinking blocks exist causes Anthropic error:
    "When thinking is disabled, an assistant message cannot contain thinking"

    Related issue: https://github.com/BerriAI/litellm/issues/18926
    """
    for message in messages:
        if message.get("role") == "assistant":
            thinking_blocks = message.get("thinking_blocks")
            if thinking_blocks is not None and (
                not hasattr(thinking_blocks, "__len__") or len(thinking_blocks) > 0
            ):
                return True
    return False

