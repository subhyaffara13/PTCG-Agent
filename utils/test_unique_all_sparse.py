
def test_unique_all_sparse():
    # https://github.com/pandas-dev/pandas/issues/23168
    arr = SparseArray([0, 0])
    result = arr.unique()
    expected = SparseArray([0])
    tm.assert_sp_array_equal(result, expected)

