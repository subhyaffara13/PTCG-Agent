
def compute_rtype_alignment(typ: RType) -> int:
    """Compute alignment of a given type based on platform alignment rule"""
    platform_alignment = PLATFORM_SIZE
    if isinstance(typ, RPrimitive):
        return typ.size
    elif isinstance(typ, RInstance):
        return platform_alignment
    elif isinstance(typ, RUnion):
        return platform_alignment
    elif isinstance(typ, RArray):
        return compute_rtype_alignment(typ.item_type)
    else:
        if isinstance(typ, RTuple):
            items = list(typ.types)
        elif isinstance(typ, RStruct):
            items = typ.types
        else:
            assert False, "invalid rtype for computing alignment"
        max_alignment = max(compute_rtype_alignment(item) for item in items)
        return max_alignment

