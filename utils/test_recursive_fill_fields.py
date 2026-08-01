
def test_recursive_fill_fields() -> None:
    a: npt.NDArray[np.void] = np.array(
        [(1, 10.0), (2, 20.0)],
        dtype=[("A", np.int64), ("B", np.float64)],
    )
    b = np.zeros((3,), dtype=a.dtype)
    out = rfn.recursive_fill_fields(a, b)
    assert_type(out, np.ndarray[tuple[int], np.dtype[np.void]])

