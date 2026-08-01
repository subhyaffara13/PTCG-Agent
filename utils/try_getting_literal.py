
def try_getting_literal(typ: Type) -> ProperType:
    """If possible, get a more precise literal type for a given type."""
    typ = get_proper_type(typ)
    if isinstance(typ, Instance) and typ.last_known_value is not None:
        return typ.last_known_value
    return typ

