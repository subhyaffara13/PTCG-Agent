
def reduce_and_conditional_type_maps(ms: list[TypeMap], *, use_meet: bool) -> TypeMap:
    """Reduces a list of TypeMaps into a single TypeMap by "and"-ing them together."""
    if len(ms) == 0:
        return {}
    if len(ms) == 1:
        return ms[0]
    result = ms[0]
    for m in ms[1:]:
        if not m:
            continue  # this is a micro-optimisation
        result = and_conditional_maps(result, m, use_meet=use_meet)
    return result

