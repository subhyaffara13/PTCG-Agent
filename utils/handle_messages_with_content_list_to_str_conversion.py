
def handle_messages_with_content_list_to_str_conversion(
    messages: List[AllMessageValues],
) -> List[AllMessageValues]:
    """
    Handles messages with content list conversion
    """
    for message in messages:
        texts = convert_content_list_to_str(message=message)
        if texts:
            message["content"] = texts
    return messages

