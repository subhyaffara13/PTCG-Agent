
def convert_content_list_to_str(
    message: Union[AllMessageValues, ChatCompletionResponseMessage],
) -> str:
    """
    - handles scenario where content is list and not string
    - content list is just text, and no images

    Motivation: mistral api + azure ai don't support content as a list
    """
    texts = ""
    message_content = message.get("content")
    if message_content:
        if message_content is not None and isinstance(message_content, list):
            for c in message_content:
                text_content = c.get("text")
                if text_content:
                    texts += text_content
        elif message_content is not None and isinstance(message_content, str):
            texts = message_content

    texts += extract_search_results_text(message.get("search_results"))
    return texts

