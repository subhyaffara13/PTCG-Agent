
def strip_thinking_blocks_from_anthropic_messages_request_dict(
    data: Dict[str, Any],
) -> None:
    """
    Mutate an Anthropic Messages-style request dict: strip thinking blocks from
    ``messages`` and remove the top-level ``thinking`` extended-thinking param.
    """
    msgs = data.get("messages")
    if isinstance(msgs, list):
        data["messages"] = strip_thinking_blocks_from_anthropic_messages(msgs)
    data.pop("thinking", None)

