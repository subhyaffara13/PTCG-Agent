
def test_drop_fields() -> None:
    ndtype = [("a", np.int64), ("b", [("b_a", np.double), ("b_b", np.int64)])]
    a = np.ones((3,), dtype=ndtype)

    assert_type(
        rfn.drop_fields(a, "a"),
        np.ndarray[tuple[int], np.dtype[np.void]],
    )
    assert_type(
        rfn.drop_fields(a, "a", asrecarray=True),
        np.rec.recarray[tuple[int], np.dtype[np.void]],
    )
    assert_type(
        rfn.rec_drop_fields(a, "a"),
        np.rec.recarray[tuple[int], np.dtype[np.void]],
    )

