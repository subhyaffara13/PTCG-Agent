
def last_assistant_with_tool_calls_has_no_thinking_blocks(
    messages: List[AllMessageValues],
) -> bool:
    """
    Returns true if the last assistant message with tool_calls has no thinking_blocks.

    This is used to detect when thinking param should be dropped to avoid
    Anthropic error: "Expected thinking or redacted_thinking, but found tool_use"

    When thinking is enabled, assistant messages with tool_calls must include thinking_blocks.
    If the client didn't preserve thinking_blocks, we need to drop the thinking param.

    IMPORTANT: This should only be used in conjunction with
    any_assistant_message_has_thinking_blocks() to ensure we don't drop thinking
    when other messages in the conversation contain thinking blocks.

    Related issues: https://github.com/BerriAI/litellm/issues/14194, https://github.com/BerriAI/litellm/issues/9020
    """
    # Find the last assistant message with tool_calls
    last_assistant_with_tools = None
    for message in messages:
        if message.get("role") == "assistant" and message.get("tool_calls") is not None:
            last_assistant_with_tools = message

    if last_assistant_with_tools is None:
        return False

    # Check if it has thinking_blocks
    thinking_blocks = last_assistant_with_tools.get("thinking_blocks")
    return thinking_blocks is None or (
        hasattr(thinking_blocks, "__len__") and len(thinking_blocks) == 0
    )

