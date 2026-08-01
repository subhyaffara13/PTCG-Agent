
def _batch_differing_spaces_multi_binary(spaces: list[MultiBinary]):
    assert all(spaces[0].shape == space.shape for space in spaces)

    return Box(
        low=0,
        high=1,
        shape=(len(spaces),) + spaces[0].shape,
        dtype=spaces[0].dtype,
        seed=deepcopy(spaces[0].np_random),
    )

