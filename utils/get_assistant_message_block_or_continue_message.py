from typing import Optional, Union

def get_assistant_message_block_or_continue_message(
    message: ChatCompletionAssistantMessage,
    assistant_continue_message: Optional[
        Union[str, ChatCompletionAssistantMessage]
    ] = None,
) -> ChatCompletionAssistantMessage:
    """
    Returns the user content block
    if content block is an empty string, then return the default continue message

    Relevant Issue: https://github.com/BerriAI/litellm/issues/7169
    """
    content_block = message.get("content", None)

    # Handle Base case
    if content_block is None or (
        assistant_continue_message is None and litellm.modify_params is False
    ):
        return skip_empty_text_blocks(message=message)

    # Handle string case
    if isinstance(content_block, str):
        # check if content is empty
        if content_block.strip():
            return message
        else:
            if is_non_content_values_set(message):
                modified_message = message.copy()
                modified_message["content"] = None
                return modified_message
            return return_assistant_continue_message(assistant_continue_message)

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
        return process_empty_text_blocks(
            message=message, assistant_continue_message=assistant_continue_message
        )

    # Handle unsupported type
    raise ValueError(f"Unsupported content type: {type(content_block)}")

