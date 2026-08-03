from typing import Any

def cmp_lt(a: Any, b: Any) -> bool:
    result = a.__lt__(b)
    if result is NotImplemented:
        raise TypeError(f"{type(a)} does not support the < operator")
    return result

