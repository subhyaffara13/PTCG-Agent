from typing import List, Optional

def _insert_user_continue_message(
    messages: List[AllMessageValues],
    user_continue_message: Optional[ChatCompletionUserMessage],
    ensure_alternating_roles: bool,
) -> List[AllMessageValues]:
    """
    Inserts a user continue message into the messages list.
    Handles three cases:
    1. Initial assistant message
    2. Final assistant message
    3. Consecutive assistant messages

    Skips tool messages and assistant messages with tool calls in the
    alternation check, matching strict templates like llama.cpp.
    """
    if not messages:
        return messages

    result_messages = messages.copy()  # Don't modify the input list
    continue_message = user_continue_message or DEFAULT_USER_CONTINUE_MESSAGE

    # Handle first message if it's an assistant message — always prepend
    # user_continue regardless of tool_calls, to preserve backward compatibility.
    if result_messages[0]["role"] == "assistant":
        result_messages.insert(0, continue_message)

    # Handle consecutive assistant messages in the counted sequence
    i = 1
    while i < len(result_messages):
        curr_message = result_messages[i]
        inserted_continue_message = False
        if (
            _counts_for_alternation(curr_message)
            and curr_message["role"] == "assistant"
        ):
            # Preserve old behavior for malformed adjacent assistant sequences like
            # assistant(tool_calls) -> assistant(no-tool-calls) with no tool message.
            if i > 0 and result_messages[i - 1].get("role") == "assistant":
                result_messages.insert(i, continue_message)
                i += 2
                inserted_continue_message = True
            else:
                j = i - 1
                while j >= 0:
                    previous_message = result_messages[j]
                    if _counts_for_alternation(previous_message):
                        if previous_message["role"] == "assistant":
                            result_messages.insert(i, continue_message)
                            i += 2
                            inserted_continue_message = True
                        break
                    j -= 1
        if not inserted_continue_message:
            i += 1

    # Handle final message — append user_continue after any trailing assistant,
    # including ones with tool_calls, to preserve backward compatibility.
    if result_messages[-1]["role"] == "assistant" and ensure_alternating_roles:
        result_messages.append(continue_message)

    return result_messages

