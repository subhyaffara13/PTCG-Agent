
def get_user_message_block_or_continue_message(
    message: ChatCompletionUserMessage,
    user_continue_message: Optional[ChatCompletionUserMessage] = None,
) -> ChatCompletionUserMessage:
    """
    Returns the user content block
    if content block is an empty string, then return the default continue message

    Relevant Issue: https://github.com/BerriAI/litellm/issues/7169
    """
    content_block = message.get("content", None)

    # Handle None case
    if content_block is None or (
        user_continue_message is None and litellm.modify_params is False
    ):
        return skip_empty_text_blocks(message=message)

    # Handle string case
    if isinstance(content_block, str):
        # check if content is empty
        if content_block.strip():
            return message
        else:
            return ChatCompletionUserMessage(
                **(user_continue_message or DEFAULT_USER_CONTINUE_MESSAGE)  # type: ignore
            )

    # Handle list case
    if isinstance(content_block, list):
        """
        CHECK FOR
            "content": [
                {
                "type": "text",
                "text": ""
                }
            ],
        """
        if not content_block:
            return ChatCompletionUserMessage(
                **(user_continue_message or DEFAULT_USER_CONTINUE_MESSAGE)  # type: ignore
            )
        # Create a copy of the message to avoid modifying the original
        modified_content_block = content_block.copy()

        for item in modified_content_block:
            # Check if the list is empty
            if item["type"] == "text":
                if not item["text"].strip():
                    # Replace empty text with continue message
                    _user_continue_message = ChatCompletionUserMessage(
                        **(user_continue_message or DEFAULT_USER_CONTINUE_MESSAGE)  # type: ignore
                    )
                    text = convert_content_list_to_str(_user_continue_message)
                    item["text"] = text
                    break
        modified_message = message.copy()
        modified_message["content"] = modified_content_block
        return modified_message

    # Handle unsupported type
    raise ValueError(f"Unsupported content type: {type(content_block)}")

