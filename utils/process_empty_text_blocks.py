from typing import List, Optional, Union

def process_empty_text_blocks(
    message: ChatCompletionAssistantMessage,
    assistant_continue_message: Optional[
        Union[str, ChatCompletionAssistantMessage]
    ] = None,
) -> ChatCompletionAssistantMessage:
    modified_content_block = message.get("content", None)
    ## BASE CASE ##
    if modified_content_block is None or not isinstance(modified_content_block, list):
        return message

    # Check if all items are empty text blocks
    if all(
        item["type"] == "text" and not item["text"].strip()
        for item in modified_content_block
    ):
        # Replace with a single continue message
        _assistant_continue_message = return_assistant_continue_message(
            assistant_continue_message
        )
        modified_content_block = [
            {
                "type": "text",
                "text": convert_content_list_to_str(_assistant_continue_message),
            }
        ]
    else:
        # Filter out only empty text blocks, keeping non-empty text and other block types
        modified_content_block = [
            item
            for item in modified_content_block
            if not (item["type"] == "text" and not item["text"].strip())
        ]

    modified_message = message.copy()
    modified_message["content"] = cast(
        Union[List[ChatCompletionTextObject], List[ChatCompletionThinkingBlock]],
        modified_content_block,
    )
    return modified_message

