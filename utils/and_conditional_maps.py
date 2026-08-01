
def and_conditional_maps(m1: TypeMap, m2: TypeMap, *, use_meet: bool = False) -> TypeMap:
    """Calculate what information we can learn from the truth of (e1 and e2)
    in terms of the information that we can learn from the truth of e1 and
    the truth of e2.
    """
    # Both conditions can be true; combine the information. Anything
    # we learn from either conditions' truth is valid.
    result = m2.copy()
    m2_exprs = {literal_hash(e2): e2 for e2 in m2}
    for e1 in m1:
        e1_hash = literal_hash(e1)
        if e1_hash not in m2_exprs:
            result[e1] = m1[e1]
            continue

        if not use_meet:
            # If use_meet=False and the same expression's type is refined by both conditions,
            # we somewhat arbitrarily give precedence to m2, unless a) m1's value is Never, or
            # b) m2's value is Any and m1 isn't a union that could have been narrowed to Any.
            t1 = m1[e1]
            pt1 = get_proper_type(t1)
            if isinstance(pt1, UninhabitedType):
                result[e1] = t1
            else:
                e2 = m2_exprs[e1_hash]
                pt2 = get_proper_type(m2[e2])
                if isinstance(pt2, AnyType) and not (
                    isinstance(pt1, UnionType)
                    and any(isinstance(get_proper_type(item), AnyType) for item in pt1.items)
                ):
                    result[e1] = t1

    if use_meet:
        # For now, meet common keys only if specifically requested.
        # This is currently used for tuple types narrowing, where having
        # a precise result is important.
        for e1 in m1:
            for e2 in m2:
                if literal_hash(e1) == literal_hash(e2):
                    result[e1] = meet_types(m1[e1], m2[e2])
    return result

