
def get_completion_messages(
    messages: List[AllMessageValues],
    assistant_continue_message: Optional[ChatCompletionAssistantMessage],
    user_continue_message: Optional[ChatCompletionUserMessage],
    ensure_alternating_roles: bool,
) -> List[AllMessageValues]:
    """
    Ensures messages alternate between user and assistant roles by adding placeholders
    only when there are consecutive messages of the same role.

    1. ensure 'user' message before 1st 'assistant' message
    2. ensure 'user' message after last 'assistant' message
    """
    if not ensure_alternating_roles:
        return messages.copy()

    ## INSERT USER CONTINUE MESSAGE
    messages = _insert_user_continue_message(
        messages, user_continue_message, ensure_alternating_roles
    )

    ## INSERT ASSISTANT CONTINUE MESSAGE
    messages = _insert_assistant_continue_message(
        messages, assistant_continue_message, ensure_alternating_roles
    )
    return messages

