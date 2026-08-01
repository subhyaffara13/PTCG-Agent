
def test_flatten_descr() -> None:
    ndtype = np.dtype([("a", "<i4"), ("b", [("b_a", "<f8"), ("b_b", "<i4")])])
    assert_type(rfn.flatten_descr(ndtype), tuple[tuple[str, np.dtype]])

