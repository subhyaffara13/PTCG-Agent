from typing import Any

def strict_float_validator(v: Any) -> float:
    if isinstance(v, float):
        return v
    raise errors.FloatError()

