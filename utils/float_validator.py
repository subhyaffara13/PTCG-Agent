from typing import Any

def float_validator(v: Any) -> float:
    if isinstance(v, float):
        return v

    try:
        return float(v)
    except (TypeError, ValueError):
        raise errors.FloatError()

