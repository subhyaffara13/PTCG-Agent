
def test_map_missing():
    arr = SparseArray([0, 1, 2])
    expected = SparseArray([10, 11, None], fill_value=10)

    result = arr.map({0: 10, 1: 11})
    tm.assert_sp_array_equal(result, expected)

