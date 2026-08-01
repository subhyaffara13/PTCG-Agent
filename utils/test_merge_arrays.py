
def test_merge_arrays() -> None:
    assert_type(
        rfn.merge_arrays((
            np.ones((2,), np.int_),
            np.ones((3,), np.float64),
        )),
        np.recarray[tuple[int], np.dtype[np.void]],
    )

