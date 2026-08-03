from typing import Any

def _unflatten_oneof(space: OneOf, x: NDArray[Any]) -> tuple[int, Any]:
    idx = np.int64(x[0])
    sub_space = space.spaces[idx]

    original_size = flatdim(sub_space)
    trimmed_sample = x[1 : 1 + original_size]

    return idx, unflatten(sub_space, trimmed_sample)

