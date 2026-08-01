
def _batch_differing_spaces_box(spaces: list[Box]):
    assert all(
        spaces[0].dtype == space.dtype for space in spaces
    ), f"Expected all dtypes to be equal, actually {[space.dtype for space in spaces]}"
    assert all(
        spaces[0].low.shape == space.low.shape for space in spaces
    ), f"Expected all Box.low shape to be equal, actually {[space.low.shape for space in spaces]}"
    assert all(
        spaces[0].high.shape == space.high.shape for space in spaces
    ), f"Expected all Box.high shape to be equal, actually {[space.high.shape for space in spaces]}"

    return Box(
        low=np.array([space.low for space in spaces]),
        high=np.array([space.high for space in spaces]),
        dtype=spaces[0].dtype,
        seed=deepcopy(spaces[0].np_random),
    )

