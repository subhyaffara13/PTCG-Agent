
def test_cumsum_integer_no_recursion():
    # GH 62669: RecursionError in integer SparseArray.cumsum
    arr = SparseArray([1, 2, 3])
    result = arr.cumsum()
    expected = SparseArray([1, 3, 6], fill_value=np.nan)
    tm.assert_sp_array_equal(result, expected)

    # Also test with some zeros interleaved
    arr2 = SparseArray([0, 1, 0, 2])
    result2 = arr2.cumsum()
    expected2 = SparseArray([0, 1, 1, 3], fill_value=np.nan)
    tm.assert_sp_array_equal(result2, expected2)

