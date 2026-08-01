
def type_vars_as_args(type_vars: Sequence[TypeVarLikeType]) -> tuple[Type, ...]:
    """Represent type variables as they would appear in a type argument list."""
    args: list[Type] = []
    for tv in type_vars:
        if isinstance(tv, TypeVarTupleType):
            args.append(UnpackType(tv))
        else:
            args.append(tv)
    return tuple(args)

