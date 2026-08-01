
def fill_typevars(typ: TypeInfo) -> Instance | TupleType:
    """For a non-generic type, return instance type representing the type.

    For a generic G type with parameters T1, .., Tn, return G[T1, ..., Tn].
    """
    tvs: list[Type] = []
    # TODO: why do we need to keep both typ.type_vars and typ.defn.type_vars?
    for i in range(len(typ.defn.type_vars)):
        tv: TypeVarLikeType | UnpackType = typ.defn.type_vars[i]
        # Change the line number
        if isinstance(tv, TypeVarType):
            tv = tv.copy_modified(line=-1, column=-1)
        elif isinstance(tv, TypeVarTupleType):
            tv = UnpackType(
                TypeVarTupleType(
                    tv.name,
                    tv.fullname,
                    tv.id,
                    tv.upper_bound,
                    tv.tuple_fallback,
                    tv.default,
                    line=-1,
                    column=-1,
                )
            )
        else:
            assert isinstance(tv, ParamSpecType)
            tv = ParamSpecType(
                tv.name,
                tv.fullname,
                tv.id,
                tv.flavor,
                tv.upper_bound,
                tv.default,
                line=-1,
                column=-1,
            )
        tvs.append(tv)
    inst = Instance(typ, tvs)
    # TODO: do we need to also handle typeddict_type here and below?
    if typ.tuple_type is None:
        return inst
    return typ.tuple_type.copy_modified(fallback=inst)

