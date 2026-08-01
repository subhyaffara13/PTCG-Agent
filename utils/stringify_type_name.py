
def stringify_type_name(typ: Type) -> str | None:
    if isinstance(typ, UnboundType):
        return typ.name
    return None

