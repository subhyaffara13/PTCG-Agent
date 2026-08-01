
def step_size(item_type: RType) -> int:
    if isinstance(item_type, RPrimitive):
        return item_type.size
    elif isinstance(item_type, RVec):
        return PLATFORM_SIZE * 2
    else:
        return PLATFORM_SIZE

