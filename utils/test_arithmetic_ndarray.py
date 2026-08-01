
def test_arithmetic_ndarray(shape, all_arithmetic_functions):
    op = all_arithmetic_functions
    a = np.zeros(shape)
    if op.__name__ == "pow":
        a += 5
    result = op(NA, a)
    expected = np.full(a.shape, NA, dtype=object)
    tm.assert_numpy_array_equal(result, expected)

