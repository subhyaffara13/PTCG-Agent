
def erased_vars(type_vars: Sequence[TypeVarLikeType], type_of_any: int) -> list[Type]:
    args: list[Type] = []
    for tv in type_vars:
        # Valid erasure for *Ts is *tuple[Any, ...], not just Any.
        if isinstance(tv, TypeVarTupleType):
            args.append(UnpackType(tv.tuple_fallback.copy_modified(args=[AnyType(type_of_any)])))
        else:
            args.append(AnyType(type_of_any))
    return args

