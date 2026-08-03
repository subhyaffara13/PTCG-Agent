from typing import Any, Tuple

def tuple_validator(v: Any) -> Tuple[Any, ...]:
    if isinstance(v, tuple):
        return v
    elif sequence_like(v):
        return tuple(v)
    else:
        raise errors.TupleError()

