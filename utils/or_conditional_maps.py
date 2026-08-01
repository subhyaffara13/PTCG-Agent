
def or_conditional_maps(m1: TypeMap, m2: TypeMap, *, coalesce_any: bool = False) -> TypeMap:
    """Calculate what information we can learn from the truth of (e1 or e2)
    in terms of the information that we can learn from the truth of e1 and
    the truth of e2. If coalesce_any is True, consider Any a supertype when
    joining restrictions.
    """

    if is_unreachable_map(m1):
        return m2
    if is_unreachable_map(m2):
        return m1
    # Both conditions can be true. Combine information about
    # expressions whose type is refined by both conditions. (We do not
    # learn anything about expressions whose type is refined by only
    # one condition.)
    result: dict[Expression, Type] = {}
    for n1 in m1:
        for n2 in m2:
            if literal_hash(n1) == literal_hash(n2):
                if coalesce_any and isinstance(get_proper_type(m1[n1]), AnyType):
                    result[n1] = m1[n1]
                else:
                    result[n1] = make_simplified_union([m1[n1], m2[n2]])
    return result

