from typing import Any

def less_than_validator(x: Any, lt: Any) -> Any:
    try:
        if not (x < lt):
            raise PydanticKnownError('less_than', {'lt': _safe_repr(lt)})
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'lt' to supplied value {x}")

