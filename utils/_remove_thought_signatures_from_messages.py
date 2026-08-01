
def _remove_thought_signatures_from_messages(
    messages: List, thought_signature_separator: str
) -> List:
    """
    Remove thought signatures from tool call IDs in all messages.
    """
    processed_messages = []

    for msg in messages:
        # Handle Pydantic models (convert to dict)
        if hasattr(msg, "model_dump"):
            msg_dict = msg.model_dump()
        elif isinstance(msg, dict):
            msg_dict = msg.copy()
        else:
            # Unknown type, keep as is
            processed_messages.append(msg)
            continue

        # Process assistant messages with tool_calls
        msg_dict = _process_assistant_message_tool_calls(
            msg_dict, thought_signature_separator
        )

        # Process tool messages with tool_call_id
        msg_dict = _process_tool_message_id(msg_dict, thought_signature_separator)

        processed_messages.append(msg_dict)

    return processed_messages

