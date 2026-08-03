from typing import Any

def less_than_or_equal_validator(x: Any, le: Any) -> Any:
    try:
        if not (x <= le):
            raise PydanticKnownError('less_than_equal', {'le': _safe_repr(le)})
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'le' to supplied value {x}")

