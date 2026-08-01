
def is_dangerous_target(typ: ProperType) -> bool:
    """Is this a dangerous target (right argument) for an isinstance() check?"""
    if isinstance(typ, TupleType):
        return any(is_dangerous_target(get_proper_type(t)) for t in typ.items)
    if isinstance(typ, FunctionLike) and typ.is_type_obj():
        return typ.type_object().has_base("mypy.types.Type")
    return False

