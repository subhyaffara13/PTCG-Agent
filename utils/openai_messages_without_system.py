
def openai_messages_without_system(
    messages: List[AllMessageValues],
) -> List[AllMessageValues]:
    return [m for m in messages if str((m or {}).get("role") or "").lower() != "system"]

