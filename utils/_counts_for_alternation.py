
def _counts_for_alternation(message: AllMessageValues) -> bool:
    role = message.get("role")
    if role == "user":
        return True
    if role == "assistant":
        return not bool(message.get("tool_calls"))
    return False

