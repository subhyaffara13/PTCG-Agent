
def trivial_join(s: Type, t: Type) -> Type:
    """Return one of types (expanded) if it is a supertype of other, otherwise top type."""
    if is_subtype(s, t):
        return t
    elif is_subtype(t, s):
        return s
    else:
        return object_or_any_from_type(get_proper_type(t))

