
def is_self_type_like(typ: Type, *, is_classmethod: bool) -> bool:
    """Does this look like a self-type annotation?"""
    typ = get_proper_type(typ)
    if not is_classmethod:
        return isinstance(typ, TypeVarType)
    if not isinstance(typ, TypeType):
        return False
    return isinstance(typ.item, TypeVarType)

