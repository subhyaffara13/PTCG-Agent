
def compute_rtype_size(typ: RType) -> int:
    """Compute unaligned size of rtype"""
    if isinstance(typ, RPrimitive):
        return typ.size
    elif isinstance(typ, RTuple):
        return compute_aligned_offsets_and_size(list(typ.types))[1]
    elif isinstance(typ, RUnion):
        return PLATFORM_SIZE
    elif isinstance(typ, RStruct):
        return compute_aligned_offsets_and_size(typ.types)[1]
    elif isinstance(typ, RInstance):
        return PLATFORM_SIZE
    elif isinstance(typ, RArray):
        alignment = compute_rtype_alignment(typ)
        aligned_size = (compute_rtype_size(typ.item_type) + (alignment - 1)) & ~(alignment - 1)
        return aligned_size * typ.length
    else:
        assert False, "invalid rtype for computing size"

