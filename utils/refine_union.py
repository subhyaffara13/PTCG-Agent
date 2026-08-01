
def refine_union(t: UnionType, s: ProperType) -> Type:
    """Refine a union type based on another type.

    This is done by refining every component of the union against the
    right hand side type (or every component of its union if it is
    one). If an element of the union is successfully refined, we drop it
    from the union in favor of the refined versions.
    """
    # Don't try to do any union refining if the types are already the
    # same.  This prevents things like refining Optional[Any] against
    # itself and producing None.
    if t == s:
        return t

    rhs_items = s.items if isinstance(s, UnionType) else [s]

    new_items = []
    for lhs in t.items:
        refined = False
        for rhs in rhs_items:
            new = refine_type(lhs, rhs)
            if new != lhs:
                new_items.append(new)
                refined = True
        if not refined:
            new_items.append(lhs)

    # Turn strict optional on when simplifying the union since we
    # don't want to drop Nones.
    with state.strict_optional_set(True):
        return make_simplified_union(new_items)

