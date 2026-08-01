
def type_info_from_type(typ: Type) -> TypeInfo | None:
    """Gets the TypeInfo for a type, indirecting through things like type variables and tuples."""
    typ = get_proper_type(typ)
    if isinstance(typ, FunctionLike) and typ.is_type_obj():
        return typ.type_object()
    if isinstance(typ, TypeType):
        typ = typ.item
    if isinstance(typ, TypeVarType):
        typ = get_proper_type(typ.upper_bound)
    if isinstance(typ, TupleType):
        typ = tuple_fallback(typ)
    if isinstance(typ, Instance):
        return typ.type

    # A complicated type. Too tricky, give up.
    # TODO: Do something more clever here.
    return None

