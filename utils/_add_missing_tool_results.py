
def _add_missing_tool_results(
    current_message: AllMessageValues,
    messages: List[AllMessageValues],
    current_index: int,
) -> Tuple[List[AllMessageValues], int]:
    """
    Case A: Missing tool_result for tool_use (orphaned tool calls)
    - If an assistant message has tool_calls but no corresponding tool result follows,
      add a dummy tool result message indicating the user did not provide the result.

    Returns:
        A tuple of:
        - List containing the assistant message, followed by existing tool results,
          followed by any dummy tool results needed
        - Number of original messages consumed (to adjust iteration index)
    """
    result_messages: List[AllMessageValues] = []
    tool_calls = current_message.get("tool_calls")

    if not tool_calls or len(cast(list, tool_calls)) == 0:
        return ([current_message], 0)

    # Collect all tool_call_ids from this assistant message
    expected_tool_call_ids = set()
    for tool_call in cast(list, tool_calls):
        tool_call_id = None
        if isinstance(tool_call, dict):
            tool_call_id = tool_call.get("id")
        else:
            tool_call_id = getattr(tool_call, "id", None)
        if tool_call_id:
            expected_tool_call_ids.add(tool_call_id)

    # Collect actual tool result messages that follow this assistant message
    found_tool_call_ids = set()
    actual_tool_results: List[AllMessageValues] = []
    j = current_index + 1

    while j < len(messages):
        next_msg = messages[j]
        next_role = next_msg.get("role")

        if next_role == "assistant":
            break

        if next_role in ["tool", "function"]:
            tool_call_id = next_msg.get("tool_call_id")
            if tool_call_id and tool_call_id in expected_tool_call_ids:
                found_tool_call_ids.add(tool_call_id)
                actual_tool_results.append(next_msg)

        j += 1

    # Find missing tool results
    missing_tool_call_ids = expected_tool_call_ids - found_tool_call_ids

    if missing_tool_call_ids:
        verbose_logger.debug(
            f"_add_missing_tool_results: Found {len(missing_tool_call_ids)} orphaned tool calls. Adding dummy tool results."
        )

        result_messages.append(current_message)

        # Add existing tool results FIRST
        result_messages.extend(actual_tool_results)

        # Then add dummy tool results for missing ones
        for tool_call_id in missing_tool_call_ids:
            tool_name = "unknown_tool"
            for tool_call in cast(list, tool_calls):
                tc_id = None
                if isinstance(tool_call, dict):
                    tc_id = tool_call.get("id")
                else:
                    tc_id = getattr(tool_call, "id", None)

                if tc_id == tool_call_id:
                    if isinstance(tool_call, dict):
                        function = tool_call.get("function", {})
                        if isinstance(function, dict):
                            tool_name = function.get("name", "unknown_tool")
                        else:
                            tool_name = getattr(function, "name", "unknown_tool")
                    else:
                        function = getattr(tool_call, "function", None)
                        if function:
                            tool_name = getattr(function, "name", "unknown_tool")
                    break

            dummy_tool_result: ChatCompletionToolMessage = {
                "role": "tool",
                "tool_call_id": tool_call_id,
                "content": f"[System: Tool execution skipped/interrupted by user. No result provided for tool '{tool_name}'.]",
            }
            result_messages.append(dummy_tool_result)

        # Return the messages and the number of original messages to skip
        return (result_messages, len(actual_tool_results))

    return ([current_message], 0)

