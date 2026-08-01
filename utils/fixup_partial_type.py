
def fixup_partial_type(typ: Type) -> Type:
    """Convert a partial type that we couldn't resolve into something concrete.

    This means, for None we make it Optional[Any], and for anything else we
    fill in all of the type arguments with Any.
    """
    if not isinstance(typ, PartialType):
        return typ
    if typ.type is None:
        return UnionType.make_union([AnyType(TypeOfAny.unannotated), NoneType()])
    else:
        return Instance(typ.type, [AnyType(TypeOfAny.unannotated)] * len(typ.type.type_vars))

