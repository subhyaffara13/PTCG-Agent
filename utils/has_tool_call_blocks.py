
def has_tool_call_blocks(messages: List[AllMessageValues]) -> bool:
    """
    Returns true, if messages has tool call blocks.

    Used for anthropic/bedrock message validation.
    """
    for message in messages:
        if message.get("tool_calls") is not None:
            return True
    return False

