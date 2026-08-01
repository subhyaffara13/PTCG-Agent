
def remove_trivial(types: Iterable[Type]) -> list[Type]:
    """Make trivial simplifications on a list of types without calling is_subtype().

    This makes following simplifications:
        * Remove bottom types (taking into account strict optional setting)
        * Remove everything else if there is an `object`
        * Remove strict duplicate types
    """
    removed_none = False
    new_types = []
    all_types = set()
    for t in types:
        p_t = get_proper_type(t)
        if isinstance(p_t, UninhabitedType):
            continue
        if isinstance(p_t, NoneType) and not state.strict_optional:
            removed_none = True
            continue
        if isinstance(p_t, Instance) and p_t.type.fullname == "builtins.object":
            return [p_t]
        if p_t not in all_types:
            new_types.append(t)
            all_types.add(p_t)
    if new_types:
        return new_types
    if removed_none:
        return [NoneType()]
    return [UninhabitedType()]

