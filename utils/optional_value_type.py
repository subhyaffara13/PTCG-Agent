
def optional_value_type(rtype: RType) -> RType | None:
    """If rtype is the union of none_rprimitive and another type X, return X.

    Otherwise, return None.
    """
    if isinstance(rtype, RUnion) and len(rtype.items) == 2:
        if rtype.items[0] == none_rprimitive:
            return rtype.items[1]
        elif rtype.items[1] == none_rprimitive:
            return rtype.items[0]
    return None

