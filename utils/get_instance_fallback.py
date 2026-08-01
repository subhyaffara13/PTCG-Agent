
def get_instance_fallback(typ: ProperType) -> list[Instance]:
    """Returns the Instance fallback for this type if one exists or None."""
    if isinstance(typ, Instance):
        return [typ]
    elif isinstance(typ, TupleType):
        return [tuple_fallback(typ)]
    elif isinstance(typ, TypedDictType):
        return [typ.fallback]
    elif isinstance(typ, FunctionLike):
        return [typ.fallback]
    elif isinstance(typ, LiteralType):
        return [typ.fallback]
    elif isinstance(typ, TypeVarType):
        if typ.values:
            res = []
            for t in typ.values:
                res.extend(get_instance_fallback(get_proper_type(t)))
            return res
        return get_instance_fallback(get_proper_type(typ.upper_bound))
    elif isinstance(typ, UnionType):
        res = []
        for t in typ.items:
            res.extend(get_instance_fallback(get_proper_type(t)))
        return res
    return []

