from typing import Any

def cmp_le(a: Any, b: Any) -> bool:
    # Check if __le__ is overridden
    if isinstance(type(a).__le__, types.FunctionType):
        return a.__le__(b)
    return cmp_eq(a, b) or cmp_lt(a, b)

