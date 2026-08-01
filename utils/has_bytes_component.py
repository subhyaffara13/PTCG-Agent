
def has_bytes_component(typ: Type) -> bool:
    """Is this one of builtin byte types, or a union that contains it?"""
    typ = get_proper_type(typ)
    byte_types = {"builtins.bytes", "builtins.bytearray"}
    if isinstance(typ, UnionType):
        return any(has_bytes_component(t) for t in typ.items)
    if isinstance(typ, Instance) and typ.type.fullname in byte_types:
        return True
    return False

