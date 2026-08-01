
def _audio_or_image_in_message_content(message: AllMessageValues) -> bool:
    """
    Checks if message content contains an image or audio
    """
    message_content = message.get("content")
    if message_content:
        if message_content is not None and isinstance(message_content, list):
            for c in message_content:
                if c.get("type") == "image_url" or c.get("type") == "input_audio":
                    return True
    return False

