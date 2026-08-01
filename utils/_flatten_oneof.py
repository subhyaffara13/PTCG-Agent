
def _flatten_oneof(space: OneOf, x: tuple[int, Any]) -> NDArray[Any]:
    idx, sample = x
    sub_space = space.spaces[idx]
    flat_sample = flatten(sub_space, sample)

    max_flatdim = flatdim(space) - 1  # Don't include the index
    if flat_sample.size < max_flatdim:
        padding = np.full(
            max_flatdim - flat_sample.size, flat_sample[0], dtype=flat_sample.dtype
        )
        flat_sample = np.concatenate([flat_sample, padding])

    return np.concatenate([[idx], flat_sample])

