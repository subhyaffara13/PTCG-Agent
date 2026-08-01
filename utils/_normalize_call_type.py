
def _normalize_call_type(call_type: Union[CallTypes, str]) -> str:
    """Return the string value for a ``CallTypes`` enum or a raw string."""
    if isinstance(call_type, CallTypes):
        return call_type.value
    return call_type

