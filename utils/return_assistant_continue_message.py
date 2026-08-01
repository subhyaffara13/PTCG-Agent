
def return_assistant_continue_message(
    assistant_continue_message: Optional[
        Union[str, ChatCompletionAssistantMessage]
    ] = None,
) -> ChatCompletionAssistantMessage:
    if assistant_continue_message and isinstance(assistant_continue_message, str):
        return ChatCompletionAssistantMessage(
            role="assistant",
            content=assistant_continue_message,
        )
    elif assistant_continue_message and isinstance(assistant_continue_message, dict):
        return ChatCompletionAssistantMessage(**assistant_continue_message)
    else:
        return DEFAULT_ASSISTANT_CONTINUE_MESSAGE

