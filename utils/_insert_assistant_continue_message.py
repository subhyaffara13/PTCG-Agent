from typing import List, Optional, Union

def _insert_assistant_continue_message(
    messages: List[AllMessageValues],
    assistant_continue_message: Optional[ChatCompletionAssistantMessage] = None,
    ensure_alternating_roles: bool = True,
) -> List[AllMessageValues]:
    """
    Add assistant continuation messages between consecutive user messages.

    Skips tool messages and assistant messages with tool calls in the
    alternation check, matching strict templates like llama.cpp.
    """
    if not ensure_alternating_roles or len(messages) <= 1:
        return messages

    continue_message = assistant_continue_message or DEFAULT_ASSISTANT_CONTINUE_MESSAGE

    # Find indexes where assistant_continue should be inserted (before that index)
    insert_before_indexes: set = set()

    for i in range(len(messages)):
        curr = messages[i]
        if _counts_for_alternation(curr) and curr["role"] == "user":
            # Look backwards for the previous counted message
            j = i - 1
            while j >= 0:
                if _counts_for_alternation(messages[j]):
                    if messages[j]["role"] == "user":
                        insert_before_indexes.add(i)
                    break
                j -= 1

    # Build the result with assistant_continue inserted at the right positions
    modified_messages: List[AllMessageValues] = []
    for i, message in enumerate(messages):
        if i in insert_before_indexes:
            modified_messages.append(continue_message)
        modified_messages.append(message)

    return modified_messages


def _insert_assistant_continue_message(
    messages: List[BedrockMessageBlock],
    assistant_continue_message: Optional[
        Union[str, ChatCompletionAssistantMessage]
    ] = None,
) -> List[BedrockMessageBlock]:
    """
    Add dummy message between user/tool result blocks.

    Conversation blocks and tool result blocks cannot be provided in the same turn. Issue: https://github.com/BerriAI/litellm/issues/6053
    """
    if assistant_continue_message is not None:
        if isinstance(assistant_continue_message, str):
            messages.append(
                BedrockMessageBlock(
                    role="assistant",
                    content=[BedrockContentBlock(text=assistant_continue_message)],
                )
            )
        elif isinstance(assistant_continue_message, dict):
            text = convert_content_list_to_str(assistant_continue_message)
            messages.append(
                BedrockMessageBlock(
                    role="assistant",
                    content=[BedrockContentBlock(text=text)],
                )
            )
    elif litellm.modify_params:
        text = convert_content_list_to_str(
            cast(ChatCompletionAssistantMessage, DEFAULT_ASSISTANT_CONTINUE_MESSAGE)
        )
        messages.append(
            BedrockMessageBlock(
                role="assistant",
                content=[
                    BedrockContentBlock(text=text),
                ],
            )
        )
    return messages

