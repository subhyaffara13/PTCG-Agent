
def _to_plain_dict(value):
    """Best-effort: coerce a value (Pydantic model / dict / None) to a dict.

    Returns the original value when no safe conversion exists. Used to bridge
    OpenAI Pydantic message/tool_call objects into the dict-based helpers.
    """
    if value is None or isinstance(value, dict):
        return value
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        try:
            return model_dump()
        except Exception:
            pass
    return value

