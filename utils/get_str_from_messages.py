
def get_str_from_messages(messages: List[AllMessageValues]) -> str:
    """
    Converts a list of messages to a string
    """
    text = ""
    for message in messages:
        text += convert_content_list_to_str(message=message)
    return text

