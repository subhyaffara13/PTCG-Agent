from typing import List

def strip_name_from_message(
    message: AllMessageValues, allowed_name_roles: List[str] = ["user"]
) -> AllMessageValues:
    """
    Removes 'name' from message
    """
    msg_copy = message.copy()
    if msg_copy.get("role") not in allowed_name_roles:
        msg_copy.pop("name", None)  # type: ignore
    return msg_copy

