from typing import Any

def type_validator(name: str, value: Any, expected_type: Any) -> None:
    """Validate that 'value' matches 'expected_type'."""
    origin = get_origin(expected_type)
    args = get_args(expected_type)

    if expected_type is Any:
        return
    elif expected_type is None:
        _validate_none(name, value)
    elif validator := _BASIC_TYPE_VALIDATORS.get(origin):
        validator(name, value, args)
    elif isinstance(expected_type, type):  # simple types
        _validate_simple_type(name, value, expected_type)
    elif isinstance(expected_type, ForwardRef) or isinstance(expected_type, str):
        return
    elif origin is Required:
        if value is _TYPED_DICT_DEFAULT_VALUE:
            raise TypeError(f"Field '{name}' is required but missing.")
        type_validator(name, value, args[0])
    elif origin is NotRequired:
        if value is _TYPED_DICT_DEFAULT_VALUE:
            return
        type_validator(name, value, args[0])
    else:
        raise TypeError(f"Unsupported type for field '{name}': {expected_type}")

