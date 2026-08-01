
def multiple_of_validator(x: Any, multiple_of: Any) -> Any:
    try:
        if x % multiple_of:
            raise PydanticKnownError('multiple_of', {'multiple_of': _safe_repr(multiple_of)})
        return x
    except TypeError:
        raise TypeError(f"Unable to apply constraint 'multiple_of' to supplied value {x}")

