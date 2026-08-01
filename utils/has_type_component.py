
def has_type_component(typ: Type, fullname: str) -> bool:
    """Is this a specific instance type, or a union that contains it?

    We use this ad-hoc function instead of a proper visitor or subtype check
    because some str vs bytes errors are strictly speaking not runtime errors,
    but rather highly counter-intuitive behavior. This is similar to what is used for
    --strict-equality.
    """
    typ = get_proper_type(typ)
    if isinstance(typ, Instance):
        return typ.type.has_base(fullname)
    elif isinstance(typ, TypeVarType):
        return has_type_component(typ.upper_bound, fullname) or any(
            has_type_component(v, fullname) for v in typ.values
        )
    elif isinstance(typ, UnionType):
        return any(has_type_component(t, fullname) for t in typ.relevant_items())
    return False

