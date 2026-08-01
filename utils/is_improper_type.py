
def is_improper_type(typ: Type) -> bool:
    """Is this a type that is not a subtype of ProperType?"""
    typ = get_proper_type(typ)
    if isinstance(typ, Instance):
        info = typ.type
        return info.has_base("mypy.types.Type") and not info.has_base("mypy.types.ProperType")
    if isinstance(typ, UnionType):
        return any(is_improper_type(t) for t in typ.items)
    return False

