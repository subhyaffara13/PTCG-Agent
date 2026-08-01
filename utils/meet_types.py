
def meet_types(s: Type, t: Type) -> ProperType:
    """Return the greatest lower bound of two types."""
    if is_recursive_pair(s, t):
        # This case can trigger an infinite recursion, general support for this will be
        # tricky, so we use a trivial meet (like for protocols).
        return trivial_meet(s, t)
    s = get_proper_type(s)
    t = get_proper_type(t)

    if isinstance(s, Instance) and isinstance(t, Instance) and s.type == t.type:
        # Code in checker.py should merge any extra_items where possible, so we
        # should have only compatible extra_items here. We check this before
        # the below subtype check, so that extra_attrs will not get erased.
        if (s.extra_attrs or t.extra_attrs) and is_same_type(s, t):
            if s.extra_attrs and t.extra_attrs:
                if len(s.extra_attrs.attrs) > len(t.extra_attrs.attrs):
                    # Return the one that has more precise information.
                    return s
                return t
            if s.extra_attrs:
                return s
            return t

    if not isinstance(s, UnboundType) and not isinstance(t, UnboundType):
        if is_proper_subtype(s, t, ignore_promotions=True):
            return s
        if is_proper_subtype(t, s, ignore_promotions=True):
            return t

    if isinstance(s, ErasedType):
        return s
    if isinstance(s, AnyType):
        return t
    if isinstance(s, UnionType) and not isinstance(t, UnionType):
        s, t = t, s

    # Meets/joins require callable type normalization.
    s, t = join.normalize_callables(s, t)

    return t.accept(TypeMeetVisitor(s))

