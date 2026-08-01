
def has_fixed_width_int(t: RType) -> bool:
    if isinstance(t, RTuple):
        return any(has_fixed_width_int(t) for t in t.types)
    elif isinstance(t, RUnion):
        return any(has_fixed_width_int(t) for t in t.items)
    return is_fixed_width_rtype(t)

