
def skip_empty_text_blocks(
    message: ChatCompletionAssistantMessage,
) -> ChatCompletionAssistantMessage:
    pass


def skip_empty_text_blocks(
    message: ChatCompletionUserMessage,
) -> ChatCompletionUserMessage:
    pass


def skip_empty_text_blocks(
    message: Union[ChatCompletionAssistantMessage, ChatCompletionUserMessage],
) -> Union[ChatCompletionAssistantMessage, ChatCompletionUserMessage]:
    """
    Skips empty text blocks in message content text blocks.

    Do not insert content here. This is a helper function, which can also be used in base case.
    """
    content_block = message.get("content", None)
    if content_block is None:
        return message
    if (
        isinstance(content_block, str)
        and not content_block.strip()
        and is_non_content_values_set(message)
        and message["role"] == "assistant"
    ):
        modified_message = message.copy()
        modified_message["content"] = None  # user message content cannot be None
        return modified_message
    elif isinstance(content_block, list):
        modified_content_block = _skip_empty_dict_blocks(
            cast(List[dict], content_block)
        )

        # If no content remains and it's an assistant message, set content to None
        if not modified_content_block and message["role"] == "assistant":
            modified_message = message.copy()
            modified_message["content"] = None
            return modified_message

        modified_message_alt = message.copy()

        # Type-specific casting based on message role
        if message["role"] == "assistant":
            modified_message_alt["content"] = cast(  # type: ignore
                Optional[List[OpenAIMessageContentListBlock]],
                modified_content_block or None,
            )
        elif message["role"] == "user" and modified_content_block is not None:
            modified_message_alt["content"] = cast(  # type: ignore
                Optional[List[ChatCompletionTextObject]], modified_content_block
            )

        return modified_message_alt

    return message

