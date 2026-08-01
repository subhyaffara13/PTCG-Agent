
def is_valid_message(message):
    """
    Check that input is a valid message in a chat, namely a dict with "role" and "content" keys.
    """
    if not isinstance(message, dict):
        return False
    if not ("role" in message and "content" in message):
        return False
    return True

