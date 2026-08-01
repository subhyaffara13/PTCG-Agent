
def _batch_differing_spaces_multi_discrete(spaces: list[MultiDiscrete]):
    assert all(
        spaces[0].dtype == space.dtype for space in spaces
    ), f"Expected all dtypes to be equal, actually {[space.dtype for space in spaces]}"
    assert all(
        spaces[0].nvec.shape == space.nvec.shape for space in spaces
    ), f"Expects all MultiDiscrete.nvec shape, actually {[space.nvec.shape for space in spaces]}"
    assert all(
        spaces[0].start.shape == space.start.shape for space in spaces
    ), f"Expects all MultiDiscrete.start shape, actually {[space.start.shape for space in spaces]}"

    return Box(
        low=np.array([space.start for space in spaces]),
        high=np.array([space.start + space.nvec for space in spaces]) - 1,
        dtype=spaces[0].dtype,
        seed=deepcopy(spaces[0].np_random),
    )

