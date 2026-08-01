
def trivial_meet(s: Type, t: Type) -> ProperType:
    """Return one of types (expanded) if it is a subtype of other, otherwise bottom type."""
    if is_subtype(s, t):
        return get_proper_type(s)
    elif is_subtype(t, s):
        return get_proper_type(t)
    else:
        if state.strict_optional:
            return UninhabitedType()
        else:
            return NoneType()

