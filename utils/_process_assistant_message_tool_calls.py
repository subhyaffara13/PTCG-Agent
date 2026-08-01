
def _process_assistant_message_tool_calls(
    msg_copy: dict, thought_signature_separator: str
) -> dict:
    """
    Process assistant message to remove thought signatures from tool call IDs.
    """
    role = msg_copy.get("role")
    tool_calls = msg_copy.get("tool_calls")

    if role == "assistant" and isinstance(tool_calls, list):
        new_tool_calls = []
        for tc in tool_calls:
            # Handle both dict and Pydantic model tool calls
            if hasattr(tc, "model_dump"):
                # It's a Pydantic model, convert to dict
                tc_dict = tc.model_dump()
            elif isinstance(tc, dict):
                tc_dict = tc.copy()
            else:
                new_tool_calls.append(tc)
                continue

            # Remove thought signature from ID if present
            if isinstance(tc_dict.get("id"), str):
                if thought_signature_separator in tc_dict["id"]:
                    tc_dict["id"] = _remove_thought_signature_from_id(
                        tc_dict["id"], thought_signature_separator
                    )

            new_tool_calls.append(tc_dict)
        msg_copy["tool_calls"] = new_tool_calls

    return msg_copy

