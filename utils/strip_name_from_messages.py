from typing import List

def strip_name_from_messages(
    messages: List[AllMessageValues], allowed_name_roles: List[str] = ["user"]
) -> List[AllMessageValues]:
    """
    Removes 'name' from messages
    """
    new_messages = []
    for message in messages:
        msg_role = message.get("role")
        msg_copy = message.copy()
        if msg_role not in allowed_name_roles:
            msg_copy.pop("name", None)  # type: ignore
        new_messages.append(msg_copy)
    return new_messages

