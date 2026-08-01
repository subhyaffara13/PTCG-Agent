
def test_with_list(op):
    arr = SparseArray([0, 1], fill_value=0)
    result = op(arr, [0, 1])
    expected = op(arr, SparseArray([0, 1]))
    tm.assert_sp_array_equal(result, expected)

