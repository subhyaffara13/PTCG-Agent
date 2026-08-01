
def test_ndmin_single_row_or_col(data, shape):
    arr = np.array([1, 2, 3, 4, 5])
    arr2d = arr.reshape(shape)

    assert_array_equal(np.loadtxt(StringIO(data), dtype=int), arr)
    assert_array_equal(np.loadtxt(StringIO(data), dtype=int, ndmin=0), arr)
    assert_array_equal(np.loadtxt(StringIO(data), dtype=int, ndmin=1), arr)
    assert_array_equal(np.loadtxt(StringIO(data), dtype=int, ndmin=2), arr2d)

