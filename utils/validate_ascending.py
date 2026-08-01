
def validate_ascending(ascending: BoolishT) -> BoolishT: ...


def validate_ascending(ascending: Sequence[BoolishT]) -> list[BoolishT]: ...


def validate_ascending(
    ascending: bool | int | Sequence[BoolishT],
) -> bool | int | list[BoolishT]:
    """Validate ``ascending`` kwargs for ``sort_index`` method."""
    kwargs = {"none_allowed": False, "int_allowed": True}
    if not isinstance(ascending, Sequence):
        return validate_bool_kwarg(ascending, "ascending", **kwargs)

    return [validate_bool_kwarg(item, "ascending", **kwargs) for item in ascending]

