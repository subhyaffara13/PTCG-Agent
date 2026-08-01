
def type_fullname(typ: Type, node: SymbolNode | None = None) -> str | None:
    typ = get_proper_type(typ)
    if isinstance(typ, Instance):
        return typ.type.fullname
    elif isinstance(typ, TypeType):
        return type_fullname(typ.item)
    elif isinstance(typ, FunctionLike) and typ.is_type_obj():
        if isinstance(node, TypeInfo):
            return node.fullname
        return type_fullname(typ.fallback)
    elif isinstance(typ, TupleType):
        return type_fullname(tuple_fallback(typ))
    elif isinstance(typ, TypeVarLikeType):
        return type_fullname(typ.upper_bound)
    return None

