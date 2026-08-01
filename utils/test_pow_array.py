
def test_pow_array(dtype):
    a = pd.array([0, 0, 0, 1, 1, 1, None, None, None], dtype=dtype)
    b = pd.array([0, 1, None, 0, 1, None, 0, 1, None], dtype=dtype)
    result = a**b
    expected = pd.array([1, 0, None, 1, 1, 1, 1, None, None], dtype=dtype)
    tm.assert_extension_array_equal(result, expected)


def test_pow_array():
    a = pd.array([0, 0, 0, 1, 1, 1, None, None, None])
    b = pd.array([0, 1, None, 0, 1, None, 0, 1, None])
    result = a**b
    expected = pd.array([1, 0, None, 1, 1, 1, 1, None, None])
    tm.assert_extension_array_equal(result, expected)

