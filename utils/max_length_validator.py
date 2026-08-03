from typing import Any

def max_length_validator(x: Any, max_length: Any) -> Any:
    try:
        if len(x) > max_length:
            raise PydanticKnownError(
                'too_long',
                {'field_type': 'Value', 'max_length': max_length, 'actual_length': len(x)},
            )
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'max_length' to supplied value {x}")

