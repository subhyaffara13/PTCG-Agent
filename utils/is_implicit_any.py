
def is_implicit_any(typ: Type) -> bool:
    typ = get_proper_type(typ)
    return isinstance(typ, AnyType) and not is_explicit_any(typ)

