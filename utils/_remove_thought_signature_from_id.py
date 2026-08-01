
def _remove_thought_signature_from_id(tool_call_id: str, separator: str) -> str:
    """
    Remove thought signature from a tool call ID.
    """
    if separator in tool_call_id:
        return tool_call_id.split(separator, 1)[0]
    return tool_call_id

