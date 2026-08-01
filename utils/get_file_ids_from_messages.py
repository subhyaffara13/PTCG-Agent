
def get_file_ids_from_messages(messages: List[AllMessageValues]) -> List[str]:
    """
    Gets file ids from messages
    """
    file_ids = []
    for message in messages:
        if message.get("role") == "user":
            content = message.get("content")
            if content:
                if isinstance(content, str):
                    continue
                for c in content:
                    if c["type"] == "file":
                        file_object = cast(ChatCompletionFileObject, c)
                        file_object_file_field = file_object.get("file")
                        if not isinstance(file_object_file_field, dict):
                            # Content block has `type: "file"` but not the
                            # OpenAI Chat Completions shape. No file_id to
                            # extract, so skip instead of raising KeyError.
                            continue
                        file_id = file_object_file_field.get("file_id")
                        if file_id:
                            file_ids.append(file_id)
    return file_ids

