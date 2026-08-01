
def get_type_range(typ: Type) -> TypeRange:
    typ = get_proper_type(typ)
    if (
        isinstance(typ, Instance)
        and typ.last_known_value
        and isinstance(typ.last_known_value.value, bool)
    ):
        typ = typ.last_known_value
    return TypeRange(typ, is_upper_bound=False)

