
def _flat_idx_to_idx(flat_idx: int, dims: tuple[int, ...]) -> tuple[int, ...]:
    idx = []
    for d in reversed(dims):
        idx.append(flat_idx % d)
        flat_idx = flat_idx // d

    return tuple(reversed(idx))

