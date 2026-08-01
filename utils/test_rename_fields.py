
def test_rename_fields() -> None:
    ndtype = [("a", np.int64), ("b", [("b_a", np.double), ("b_b", np.int64)])]
    a = np.ones((3,), dtype=ndtype)

    assert_type(
        rfn.rename_fields(a, {"a": "A", "b_b": "B_B"}),
        np.ndarray[tuple[int], np.dtype[np.void]],
    )

