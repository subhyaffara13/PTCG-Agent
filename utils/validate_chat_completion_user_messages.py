
def validate_chat_completion_user_messages(messages: List[AllMessageValues]):
    """
    Ensures all user messages are valid OpenAI chat completion messages.

    Args:
        messages: List of message dictionaries
        message_content_type: Type to validate content against

    Returns:
        List[dict]: The validated messages

    Raises:
        ValueError: If any message is invalid
    """
    for idx, m in enumerate(messages):
        try:
            if m["role"] == "user":
                user_content = m.get("content")
                if user_content is not None:
                    if isinstance(user_content, str):
                        continue
                    elif isinstance(user_content, list):
                        for item in user_content:
                            if isinstance(item, dict):
                                if item.get("type") not in ValidUserMessageContentTypes:
                                    raise Exception(
                                        f"invalid content type={item.get('type')}"
                                    )
        except Exception as e:
            if isinstance(e, KeyError):
                raise Exception(
                    f"Invalid message at index {idx}. Please ensure all messages are valid OpenAI chat completion messages."
                )
            if "invalid content type" in str(e):
                raise Exception(
                    f"Invalid user message at index {idx}. Please ensure all user messages are valid OpenAI chat completion messages."
                )
            else:
                raise e

    return messages

