
def _default_user_message_when_system_message_passed() -> ChatCompletionUserMessage:
    """
    Returns a default user message when a "system" message is passed in gemini fails.

    This adds a blank user message to the messages list, to ensure that gemini doesn't fail the request.
    """
    return ChatCompletionUserMessage(content=".", role="user")

