
def test_assign_fields_by_name() -> None:
    b = np.ones(4, dtype=[("x", "i4"), ("y", "f4"), ("z", "f8")])
    assert_type(
        rfn.apply_along_fields(np.mean, b),
        np.ndarray[tuple[int], np.dtype[np.void]],
    )

