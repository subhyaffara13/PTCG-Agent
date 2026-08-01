
def test_vector_norm():
    x = np.arange(9).reshape((3, 3))
    actual = np.linalg.vector_norm(x)

    assert_almost_equal(actual, np.float64(14.2828), double_decimal=3)

    actual = np.linalg.vector_norm(x, axis=0)

    assert_almost_equal(
        actual, np.array([6.7082, 8.124, 9.6436]), double_decimal=3
    )

    actual = np.linalg.vector_norm(x, keepdims=True)
    expected = np.full((1, 1), 14.2828, dtype='float64')
    assert_equal(actual.shape, expected.shape)
    assert_almost_equal(actual, expected, double_decimal=3)

