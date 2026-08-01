
def _flatten_multidiscrete(
    space: MultiDiscrete, x: NDArray[np.int64]
) -> NDArray[np.int64]:
    offsets = np.zeros((space.nvec.size + 1,), dtype=np.int32)
    offsets[1:] = np.cumsum(space.nvec.flatten())

    onehot = np.zeros((offsets[-1],), dtype=space.dtype)
    onehot[offsets[:-1] + (x - space.start).flatten()] = 1
    return onehot


def _flatten_multidiscrete(space, x) -> np.ndarray:
    offsets = np.zeros((space.nvec.size + 1,), dtype=space.dtype)
    offsets[1:] = np.cumsum(space.nvec.flatten())

    onehot = np.zeros((offsets[-1],), dtype=space.dtype)
    onehot[offsets[:-1] + x.flatten()] = 1
    return onehot

