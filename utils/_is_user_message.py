
def _is_user_message(msg: Any) -> bool:
    return isinstance(msg, dict) and msg.get("role") == "user"

