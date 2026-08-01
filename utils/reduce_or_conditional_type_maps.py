
def reduce_or_conditional_type_maps(ms: list[TypeMap]) -> TypeMap:
    """Reduces a list of TypeMaps into a single TypeMap by "or"-ing them together."""
    if len(ms) == 0:
        return {}
    if len(ms) == 1:
        return ms[0]
    result = ms[0]
    for m in ms[1:]:
        result = or_conditional_maps(result, m)
    return result

