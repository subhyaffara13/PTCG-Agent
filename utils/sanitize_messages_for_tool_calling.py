from typing import Dict, List, Set

def sanitize_messages_for_tool_calling(
    messages: List[AllMessageValues],
) -> List[AllMessageValues]:
    """
    Sanitize messages for tool calling to handle common issues when modify_params=True:

    Case A: Missing tool_result for tool_use (orphaned tool calls)
    - If an assistant message has tool_calls but no corresponding tool result follows,
      add a dummy tool result message indicating the user did not provide the result.

    Case B: Orphaned tool_result (unexpected result)
    - If a tool message references a tool_call_id that doesn't exist in the previous
      assistant message, remove that tool message.

    Case C: Empty text content
    - Replace empty or whitespace-only text content with a placeholder message.

    Case D: Duplicate tool_result for same tool_use (duplicate results)
    - If multiple tool messages reference the same tool_call_id, keep only the last
      occurrence. Anthropic requires exactly one tool_result per tool_use and rejects
      with: "each tool_use must have a single result".

    This function operates on OpenAI format messages before they are converted to
    provider-specific formats.
    """
    if not litellm.modify_params:
        return messages

    sanitized_messages: List[AllMessageValues] = []
    i = 0

    while i < len(messages):
        current_message = messages[i]

        # Case C: Sanitize empty text content
        current_message = _sanitize_empty_text_content(current_message)

        # Case A: Check if assistant message has tool_calls without following tool results
        if current_message.get("role") == "assistant":
            result_messages, messages_consumed = _add_missing_tool_results(
                current_message, messages, i
            )

            # If dummy tool results were added, extend sanitized_messages and skip consumed messages
            if len(result_messages) > 1:
                sanitized_messages.extend(result_messages)
                # Skip the assistant message and any actual tool results that were included
                i += 1 + messages_consumed
                continue

        # Case B: Check for orphaned tool results
        if _is_orphaned_tool_result(current_message, sanitized_messages):
            i += 1
            continue  # Skip this orphaned tool result

        # Add the message to sanitized list
        sanitized_messages.append(current_message)
        i += 1

    # Case D: Deduplicate tool results with the same tool_call_id.
    # Anthropic requires exactly one tool_result per tool_use. Session history
    # (e.g. from conversation resume) can contain duplicate tool_result messages
    # for the same tool_call_id. Keep only the last occurrence *within each
    # contiguous block of tool results following an assistant message*. This
    # avoids dropping results from earlier turns if a tool_call_id is reused.
    #
    # NOTE: This intentionally keeps the *last* occurrence (most complete for
    # session-resume duplicates), unlike _deduplicate_bedrock_content_blocks
    # which keeps the *first*. The Bedrock case handles provider-side content
    # block duplication where the first is authoritative; here the duplicate
    # arises from history replay where the last entry is the final state.
    duplicates_to_remove: Set[int] = set()
    seen_in_block: Dict[str, int] = {}  # tool_call_id -> index (reset per block)
    for idx, msg in enumerate(sanitized_messages):
        role = msg.get("role")
        tcid = msg.get("tool_call_id") if role in ["tool", "function"] else None
        if tcid and isinstance(tcid, str):
            if tcid in seen_in_block:
                # Mark the earlier occurrence for removal (keep latest)
                duplicates_to_remove.add(seen_in_block[tcid])
                verbose_logger.warning(
                    "sanitize_messages_for_tool_calling: dropping duplicate "
                    "tool_result with tool_call_id=%s. This may indicate "
                    "duplicate tool messages in conversation history.",
                    tcid,
                )
            seen_in_block[tcid] = idx
        elif role not in ("tool", "function"):
            # Non-tool message (user, assistant, system) marks a
            # conversational-turn boundary — reset tracking.
            # Tool/function messages with no tool_call_id are malformed;
            # they should NOT reset the block because they don't represent
            # a turn boundary and would mask real within-block duplicates.
            seen_in_block = {}

    if duplicates_to_remove:
        sanitized_messages = [
            msg
            for idx, msg in enumerate(sanitized_messages)
            if idx not in duplicates_to_remove
        ]

    return sanitized_messages

