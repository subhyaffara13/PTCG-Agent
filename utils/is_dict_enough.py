from typing import Any

def isDictEnough(value: Any) -> bool:
    """
    Some objects will likely come in that aren't
    dicts but are dict-ish enough.
    """
    if isinstance(value, Mapping):
        return True
    for attr in ("keys", "values", "items"):
        if not hasattr(value, attr):
            return False
    return True

