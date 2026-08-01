
def safe_meet(t: Type, s: Type) -> Type:
    # Similar to above but for meet_types().
    from mypy.meet import meet_types

    if not isinstance(t, UnpackType) and not isinstance(s, UnpackType):
        return meet_types(t, s)
    if isinstance(t, UnpackType) and isinstance(s, UnpackType):
        unpacked = get_proper_type(t.type)
        if isinstance(unpacked, TypeVarTupleType):
            fallback_type = unpacked.tuple_fallback.type
        elif isinstance(unpacked, TupleType):
            fallback_type = unpacked.partial_fallback.type
        else:
            assert isinstance(unpacked, Instance) and unpacked.type.fullname == "builtins.tuple"
            fallback_type = unpacked.type
        res = meet_types(t.type, s.type)
        if isinstance(res, UninhabitedType):
            res = Instance(fallback_type, [res])
        return UnpackType(res)
    return UninhabitedType()

