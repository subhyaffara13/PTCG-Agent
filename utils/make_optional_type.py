
def make_optional_type(t: Type) -> Type:
    """Return the type corresponding to Optional[t].

    Note that we can't use normal union simplification, since this function
    is called during semantic analysis and simplification only works during
    type checking.
    """
    if isinstance(t, ProperType) and isinstance(t, NoneType):
        return t
    elif isinstance(t, ProperType) and isinstance(t, UnionType):
        # Eagerly expanding aliases is not safe during semantic analysis.
        items = [item for item in t.items if not isinstance(get_proper_type(item), NoneType)]
        return UnionType(items + [NoneType()], t.line, t.column)
    else:
        return UnionType([t, NoneType()], t.line, t.column)

