
def can_coerce_to(src: RType, dest: RType) -> bool:
    """Check if src can be assigned to dest_rtype.

    Currently okay to have false positives.
    """
    if isinstance(dest, RUnion):
        return any(can_coerce_to(src, d) for d in dest.items)

    if isinstance(dest, RPrimitive):
        if isinstance(src, RPrimitive):
            # If either src or dest is a disjoint type, then they must both be.
            if src.name in disjoint_types and dest.name in disjoint_types:
                return src.name == dest.name
            return src.size == dest.size
        if isinstance(src, (RInstance, RVec)):
            return is_object_rprimitive(dest)
        if isinstance(src, RUnion):
            # IR doesn't have the ability to narrow unions based on
            # control flow, so cannot be a strict all() here.
            return any(can_coerce_to(s, dest) for s in src.items)
        return False

    return True

