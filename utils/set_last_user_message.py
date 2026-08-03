from typing import List

def set_last_user_message(
    messages: List[AllMessageValues], content: str
) -> List[AllMessageValues]:
    """
    Set the last user message

    1. remove all the last consecutive user messages (FROM THE END)
    2. add the new message
    """
    idx_to_remove = []
    for idx, message in enumerate(reversed(messages)):
        if message.get("role") == "user":
            idx_to_remove.append(idx)
        else:
            # Stop when we hit a non-user message
            break
    if idx_to_remove:
        messages = [
            message
            for idx, message in enumerate(reversed(messages))
            if idx not in idx_to_remove
        ]
        messages.reverse()
    messages.append({"role": "user", "content": content})
    return messages

