
def test_numpy_argwhere(index):
    # GH#35331

    s = Series(range(5), index=index, dtype=np.int64)

    result = np.argwhere(s > 2).astype(np.int64)
    expected = np.array([[3], [4]], dtype=np.int64)

    tm.assert_numpy_array_equal(result, expected)

