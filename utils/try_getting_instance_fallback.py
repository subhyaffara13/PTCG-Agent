
def try_getting_instance_fallback(typ: Type) -> Instance | None:
    """Returns the Instance fallback for this type if one exists or None."""
    typ = get_proper_type(typ)
    if isinstance(typ, Instance):
        return typ
    elif isinstance(typ, LiteralType):
        return typ.fallback
    elif isinstance(typ, (NoneType, AnyType)):
        return None  # Fast path for None, which is common
    elif isinstance(typ, FunctionLike):
        return typ.fallback
    elif isinstance(typ, TypeVarType):
        return try_getting_instance_fallback(typ.upper_bound)
    elif isinstance(typ, TupleType):
        return typ.partial_fallback
    elif isinstance(typ, TypedDictType):
        return typ.fallback
    return None

