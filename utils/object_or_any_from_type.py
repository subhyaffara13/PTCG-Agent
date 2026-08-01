
def object_or_any_from_type(typ: ProperType) -> ProperType:
    # Similar to object_from_instance() but tries hard for all types.
    # TODO: find a better way to get object, or make this more reliable.
    if isinstance(typ, Instance):
        return object_from_instance(typ)
    elif isinstance(typ, (CallableType, TypedDictType, LiteralType)):
        return object_from_instance(typ.fallback)
    elif isinstance(typ, TupleType):
        return object_from_instance(typ.partial_fallback)
    elif isinstance(typ, TypeType):
        return object_or_any_from_type(typ.item)
    elif isinstance(typ, TypeVarLikeType) and isinstance(typ.upper_bound, ProperType):
        return object_or_any_from_type(typ.upper_bound)
    elif isinstance(typ, UnionType):
        for item in typ.items:
            if isinstance(item, ProperType):
                candidate = object_or_any_from_type(item)
                if isinstance(candidate, Instance):
                    return candidate
    elif isinstance(typ, UnpackType):
        object_or_any_from_type(get_proper_type(typ.type))
    return AnyType(TypeOfAny.implementation_artifact)

