
def test_numpy_zero_dim_ndarray(other):
    arr = pd.array([1, None, 2])
    result = arr + np.array(other)
    expected = arr + other
    tm.assert_equal(result, expected)

