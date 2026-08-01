
def test_arith_zero_dim_ndarray(other):
    arr = pd.array([1, None, 2], dtype="Float64")
    result = arr + np.array(other)
    expected = arr + other
    tm.assert_equal(result, expected)

