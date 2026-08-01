
def _batch_space_multidiscrete(space: MultiDiscrete, n: int = 1):
    repeats = tuple([n] + [1] * space.nvec.ndim)
    low = np.tile(space.start, repeats)
    high = low + np.tile(space.nvec, repeats) - 1
    return Box(
        low=low,
        high=high,
        dtype=space.dtype,
        seed=deepcopy(space.np_random),
    )


def _batch_space_multidiscrete(space, n=1):
    repeats = tuple([n] + [1] * space.nvec.ndim)
    high = np.tile(space.nvec, repeats) - 1
    return Box(
        low=np.zeros_like(high),
        high=high,
        dtype=space.dtype,
        seed=deepcopy(space.np_random),
    )

