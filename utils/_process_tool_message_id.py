
def _process_tool_message_id(msg_copy: dict, thought_signature_separator: str) -> dict:
    """
    Process tool message to remove thought signature from tool_call_id.
    """
    if msg_copy.get("role") == "tool" and isinstance(msg_copy.get("tool_call_id"), str):
        if thought_signature_separator in msg_copy["tool_call_id"]:
            msg_copy["tool_call_id"] = _remove_thought_signature_from_id(
                msg_copy["tool_call_id"], thought_signature_separator
            )

    return msg_copy

