
def _flatten_space_oneof(space: OneOf) -> Box:
    num_subspaces = len(space.spaces)
    max_flatdim = max(flatdim(s) for s in space.spaces) + 1

    lows = np.array([np.min(flatten_space(s).low) for s in space.spaces])
    highs = np.array([np.max(flatten_space(s).high) for s in space.spaces])

    overall_low = np.min(lows)
    overall_high = np.max(highs)

    low = np.concatenate([[0], np.full(max_flatdim - 1, overall_low)])
    high = np.concatenate([[num_subspaces - 1], np.full(max_flatdim - 1, overall_high)])

    dtype = np.result_type(*[s.dtype for s in space.spaces if hasattr(s, "dtype")])
    return Box(low=low, high=high, shape=(max_flatdim,), dtype=dtype)

