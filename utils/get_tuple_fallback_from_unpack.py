
def get_tuple_fallback_from_unpack(unpack: UnpackType) -> TypeInfo:
    """Get builtins.tuple type from available types to construct homogeneous tuples."""
    tp = get_proper_type(unpack.type)
    if isinstance(tp, Instance) and tp.type.fullname == "builtins.tuple":
        return tp.type
    if isinstance(tp, TypeVarTupleType):
        return tp.tuple_fallback.type
    if isinstance(tp, TupleType):
        for base in tp.partial_fallback.type.mro:
            if base.fullname == "builtins.tuple":
                return base
    assert False, "Invalid unpack type"

