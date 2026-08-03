from typing import Any

def strict_int_validator(v: Any) -> int:
    if isinstance(v, int) and not (v is True or v is False):
        return v
    raise errors.IntegerError()

