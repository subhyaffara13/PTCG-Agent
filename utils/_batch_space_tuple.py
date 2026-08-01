
def _batch_space_tuple(space: Tuple, n: int = 1):
    return Tuple(
        tuple(batch_space(subspace, n=n) for subspace in space.spaces),
        seed=deepcopy(space.np_random),
    )


def _batch_space_tuple(space, n=1):
    return Tuple(
        tuple(batch_space(subspace, n=n) for subspace in space.spaces),
        seed=deepcopy(space.np_random),
    )

