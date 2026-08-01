
def is_descriptor(typ: Type | None) -> bool:
    typ = get_proper_type(typ)
    if isinstance(typ, Instance):
        return typ.type.get("__get__") is not None
    if isinstance(typ, UnionType):
        return all(is_descriptor(item) for item in typ.relevant_items())
    return False

