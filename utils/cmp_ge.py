from typing import Any

def cmp_ge(a: Any, b: Any) -> bool:
    # Check if __ge__ is overridden
    if isinstance(type(a).__ge__, types.FunctionType):
        return a.__ge__(b)
    return cmp_eq(a, b) or cmp_gt(a, b)

