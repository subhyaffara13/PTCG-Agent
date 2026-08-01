
def test_valid_input(indexer, expected):
    arr = np.array([1, 2, 3])
    result = check_array_indexer(arr, indexer)
    tm.assert_numpy_array_equal(result, expected)

