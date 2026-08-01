
def test_stack_arrays() -> None:
    x = np.zeros((2,), np.int32)
    assert_type(
        rfn.stack_arrays(x),
        np.ndarray[tuple[int], np.dtype[np.int32]],
    )

    z = np.ones((2,), [("A", "|S3"), ("B", float)])
    zz = np.ones((2,), [("A", "|S3"), ("B", np.float64), ("C", np.float64)])
    assert_type(
        rfn.stack_arrays((z, zz)),
        np.ma.MaskedArray[tuple[Any, ...], np.dtype[np.void]],
    )

