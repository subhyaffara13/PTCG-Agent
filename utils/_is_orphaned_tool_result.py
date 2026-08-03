from typing import List

def _is_orphaned_tool_result(
    current_message: AllMessageValues,
    sanitized_messages: List[AllMessageValues],
) -> bool:
    """
    Case B: Orphaned tool_result (unexpected result)
    - Check if a tool message references a tool_call_id that doesn't exist in the previous
      assistant message.

    Returns:
        True if this is an orphaned tool result that should be removed, False otherwise
    """
    if current_message.get("role") not in ["tool", "function"]:
        return False

    tool_call_id = current_message.get("tool_call_id")

    if not tool_call_id:
        return False

    # Look back to find the most recent assistant message with tool_calls
    found_matching_tool_call = False

    for j in range(len(sanitized_messages) - 1, -1, -1):
        prev_msg = sanitized_messages[j]
        if prev_msg.get("role") == "assistant":
            tool_calls = prev_msg.get("tool_calls")
            if tool_calls:
                for tool_call in cast(list, tool_calls):
                    tc_id = None
                    if isinstance(tool_call, dict):
                        tc_id = tool_call.get("id")
                    else:
                        tc_id = getattr(tool_call, "id", None)

                    if tc_id == tool_call_id:
                        found_matching_tool_call = True
                        break

            break

    if not found_matching_tool_call:
        verbose_logger.debug(
            "_is_orphaned_tool_result: Found orphaned tool result with redacted tool_call_id"
        )
        return True

    return False

