
def resolve_operation(call_type: str | None) -> GenAIOperation:
    """Map a litellm ``call_type`` to a ``gen_ai.operation.name`` value."""
    if not call_type:
        return GenAIOperation.CHAT
    return _OPERATION_BY_CALL_TYPE.get(call_type.lower(), GenAIOperation.CHAT)

