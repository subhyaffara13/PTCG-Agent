from typing import Any

def greater_than_or_equal_validator(x: Any, ge: Any) -> Any:
    try:
        if not (x >= ge):
            raise PydanticKnownError('greater_than_equal', {'ge': _safe_repr(ge)})
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'ge' to supplied value {x}")

