
def min_length_validator(x: Any, min_length: Any) -> Any:
    try:
        if not (len(x) >= min_length):
            raise PydanticKnownError(
                'too_short', {'field_type': 'Value', 'min_length': min_length, 'actual_length': len(x)}
            )
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'min_length' to supplied value {x}")

