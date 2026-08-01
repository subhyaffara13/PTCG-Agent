
def _literal_type_check(value: Any, /) -> None:
    """Type check the provided literal value against the legal parameters."""
    if (
        not isinstance(value, (int, bytes, str, bool, Enum, typing_objects.NoneType))
        and value is not typing_objects.NoneType
    ):
        raise TypeError(f'{value} is not a valid literal value, must be one of: int, bytes, str, Enum, None.')

