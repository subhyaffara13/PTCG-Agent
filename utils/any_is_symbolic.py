from typing import Any

def any_is_symbolic(*args: Any) -> bool:
    return any(is_symbolic(a) for a in args)

