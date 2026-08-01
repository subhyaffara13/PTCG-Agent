
def restrict_subtype_away(t: Type, s: Type, *, consider_runtime_isinstance: bool = True) -> Type:
    """Return t minus s for runtime type assertions.

    If we can't determine a precise result, return a supertype of the
    ideal result (just t is a valid result).

    This is used for type inference of runtime type checks such as
    isinstance(). Currently, this just removes elements of a union type.
    """
    p_t = get_proper_type(t)
    if isinstance(p_t, UnionType):
        new_items = try_restrict_literal_union(p_t, s)
        if new_items is None:
            new_items = [
                restrict_subtype_away(
                    item, s, consider_runtime_isinstance=consider_runtime_isinstance
                )
                for item in p_t.relevant_items()
            ]
        return UnionType.make_union(
            [item for item in new_items if not isinstance(get_proper_type(item), UninhabitedType)]
        )
    elif isinstance(p_t, TypeVarType):
        return p_t.copy_modified(upper_bound=restrict_subtype_away(p_t.upper_bound, s))

    if consider_runtime_isinstance:
        if covers_at_runtime(t, s):
            return UninhabitedType()
        else:
            return t
    else:
        if is_proper_subtype(t, s, ignore_promotions=True):
            return UninhabitedType()
        if is_proper_subtype(t, s, ignore_promotions=True, erase_instances=True):
            return UninhabitedType()
        return t

