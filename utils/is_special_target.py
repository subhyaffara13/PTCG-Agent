
def is_special_target(right: ProperType) -> bool:
    """Whitelist some special cases for use in isinstance() with improper types."""
    if isinstance(right, FunctionLike) and right.is_type_obj():
        if right.type_object().fullname == "builtins.tuple":
            # Used with Union[Type, Tuple[Type, ...]].
            return True
        if right.type_object().fullname in (
            "mypy.types.Type",
            "mypy.types.ProperType",
            "mypy.types.TypeAliasType",
        ):
            # Special case: things like assert isinstance(typ, ProperType) are always OK.
            return True
        if right.type_object().fullname in (
            "mypy.types.UnboundType",
            "mypy.types.TypeVarLikeType",
            "mypy.types.TypeVarType",
            "mypy.types.UnpackType",
            "mypy.types.TypeVarTupleType",
            "mypy.types.ParamSpecType",
            "mypy.types.Parameters",
            "mypy.types.RawExpressionType",
            "mypy.types.EllipsisType",
            "mypy.types.StarType",
            "mypy.types.TypeList",
            "mypy.types.CallableArgument",
            "mypy.types.PartialType",
            "mypy.types.ErasedType",
            "mypy.types.DeletedType",
            "mypy.types.RequiredType",
            "mypy.types.ReadOnlyType",
            "mypy.types.TypeGuardedType",
            "mypy.types.PlaceholderType",
        ):
            # Special case: these are not valid targets for a type alias and thus safe.
            # TODO: introduce a SyntheticType base to simplify this?
            return True
    elif isinstance(right, TupleType):
        return all(is_special_target(t) for t in get_proper_types(right.items))
    return False

