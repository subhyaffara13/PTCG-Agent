
def _batch_space_dict(space: Dict, n: int = 1):
    return Dict(
        {key: batch_space(subspace, n=n) for key, subspace in space.items()},
        seed=deepcopy(space.np_random),
    )


def _batch_space_dict(space, n=1):
    return Dict(
        OrderedDict(
            [
                (key, batch_space(subspace, n=n))
                for (key, subspace) in space.spaces.items()
            ]
        ),
        seed=deepcopy(space.np_random),
    )

