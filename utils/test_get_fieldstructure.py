
def test_get_fieldstructure() -> None:
    ndtype = np.dtype([
        ("A", int),
        ("B", [("B_A", int), ("B_B", [("B_B_A", int), ("B_B_B", int)])]),
    ])
    assert_type(rfn.get_fieldstructure(ndtype), dict[str, list[str]])

