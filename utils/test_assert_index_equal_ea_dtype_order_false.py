
def test_assert_index_equal_ea_dtype_order_false(any_numeric_ea_dtype):
    # GH#47207
    idx1 = Index([1, 3], dtype=any_numeric_ea_dtype)
    idx2 = Index([3, 1], dtype=any_numeric_ea_dtype)
    tm.assert_index_equal(idx1, idx2, check_order=False)

