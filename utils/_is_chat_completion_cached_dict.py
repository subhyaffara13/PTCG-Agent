
def _is_chat_completion_cached_dict(cached_result: dict) -> bool:
    cached_id = cached_result.get("id")
    if isinstance(cached_id, str) and cached_id.startswith("chatcmpl"):
        return True
    obj = cached_result.get("object")
    if isinstance(obj, str):
        return obj.startswith("chat.completion")
    return "choices" in cached_result

