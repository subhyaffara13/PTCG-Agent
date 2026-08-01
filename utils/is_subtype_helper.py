
def is_subtype_helper(left: mypy.types.Type, right: mypy.types.Type) -> bool:
    """Checks whether ``left`` is a subtype of ``right``."""
    left = _relax_type_check_only_type(mypy.types.get_proper_type(left))
    right = _relax_type_check_only_type(mypy.types.get_proper_type(right))
    if (
        isinstance(left, mypy.types.LiteralType)
        and isinstance(left.value, int)
        and left.value in (0, 1)
        and mypy.types.is_named_instance(right, "builtins.bool")
    ):
        # Pretend Literal[0, 1] is a subtype of bool to avoid unhelpful errors.
        return True

    if isinstance(right, mypy.types.TypedDictType) and mypy.types.is_named_instance(
        left, "builtins.dict"
    ):
        # Special case checks against TypedDicts
        return True

    with mypy.state.state.strict_optional_set(True):
        return mypy.subtypes.is_subtype(left, right)

