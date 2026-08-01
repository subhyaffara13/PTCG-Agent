
def test_duplicated(idx_dup, keep, expected):
    result = idx_dup.duplicated(keep=keep)
    expected = np.array(expected)
    tm.assert_numpy_array_equal(result, expected)

