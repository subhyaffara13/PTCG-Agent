
def coerce_to_literal(typ: Type) -> Type:
    """Recursively converts any Instances that have a last_known_value or are
    instances of enum types with a single value into the corresponding LiteralType.
    """
    original_type = typ
    typ = get_proper_type(typ)
    if isinstance(typ, UnionType):
        new_items = [coerce_to_literal(item) for item in typ.items]
        return UnionType.make_union(new_items)
    elif isinstance(typ, Instance):
        if typ.last_known_value:
            return typ.last_known_value
        elif typ.type.is_enum:
            enum_values = typ.type.enum_members
            if len(enum_values) == 1:
                return LiteralType(value=enum_values[0], fallback=typ)
    return original_type

