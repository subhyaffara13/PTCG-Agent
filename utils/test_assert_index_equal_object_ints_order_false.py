
def test_assert_index_equal_object_ints_order_false():
    # GH#47207
    idx1 = Index([1, 3], dtype="object")
    idx2 = Index([3, 1], dtype="object")
    tm.assert_index_equal(idx1, idx2, check_order=False)

