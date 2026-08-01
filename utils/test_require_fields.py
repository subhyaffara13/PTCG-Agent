
def test_require_fields() -> None:
    a = np.ones(4, dtype=[("a", "i4"), ("b", "f8"), ("c", "u1")])
    assert_type(
        rfn.require_fields(a, [("b", "f4"), ("c", "u1")]),
        np.ndarray[tuple[int], np.dtype[np.void]],
    )

