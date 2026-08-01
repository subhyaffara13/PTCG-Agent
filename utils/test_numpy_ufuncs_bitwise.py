
def test_numpy_ufuncs_bitwise(func):
    # https://github.com/pandas-dev/pandas/issues/46769
    idx1 = Index([1, 2, 3, 4], dtype="int64")
    idx2 = Index([3, 4, 5, 6], dtype="int64")

    with tm.assert_produces_warning(None):
        result = func(idx1, idx2)

    expected = Index(func(idx1.values, idx2.values))
    tm.assert_index_equal(result, expected)

