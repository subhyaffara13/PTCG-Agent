
def _batch_space_discrete(space: Discrete, n: int = 1):
    return MultiDiscrete(
        np.full((n,), space.n, dtype=space.dtype),
        dtype=space.dtype,
        seed=deepcopy(space.np_random),
        start=np.full((n,), space.start, dtype=space.dtype),
    )


def _batch_space_discrete(space, n=1):
    if space.start == 0:
        return MultiDiscrete(
            np.full((n,), space.n, dtype=space.dtype),
            dtype=space.dtype,
            seed=deepcopy(space.np_random),
        )
    else:
        return Box(
            low=space.start,
            high=space.start + space.n - 1,
            shape=(n,),
            dtype=space.dtype,
            seed=deepcopy(space.np_random),
        )

