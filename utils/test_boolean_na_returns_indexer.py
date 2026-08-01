
def test_boolean_na_returns_indexer(indexer):
    # https://github.com/pandas-dev/pandas/issues/31503
    arr = np.array([1, 2, 3])

    result = check_array_indexer(arr, indexer)
    expected = np.array([True, False, False], dtype=bool)

    tm.assert_numpy_array_equal(result, expected)

