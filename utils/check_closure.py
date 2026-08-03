from typing import Any

def check_closure(value: Any, metadata: Any) -> bool:
    if type(value) is types.FunctionType and hasattr(value, "__code__"):
        return value.__code__ is metadata
    return id(value) == metadata

