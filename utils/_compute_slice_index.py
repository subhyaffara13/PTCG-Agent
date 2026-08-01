
def _compute_slice_index(size: IntLikeType, index: IntLikeType) -> IntLikeType | None:
    from torch.fx.experimental.symbolic_shapes import guard_or_false, sym_and

    if guard_or_false(sym_and(index >= 0, index <= size)):
        return index
    elif guard_or_false(sym_and(index < 0, index >= -size)):
        return index + size
    elif guard_or_false(index < -size):
        return 0
    elif guard_or_false(index > size):
        return size
    elif guard_or_false(index >= 0):
        return torch.sym_min(index, size)
    elif guard_or_false(index < 0):
        return torch.sym_max(index + size, 0)

    return None

