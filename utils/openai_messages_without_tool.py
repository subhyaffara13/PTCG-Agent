
def openai_messages_without_tool(
    messages: List[AllMessageValues],
) -> List[AllMessageValues]:
    return [m for m in messages if str((m or {}).get("role") or "").lower() != "tool"]

