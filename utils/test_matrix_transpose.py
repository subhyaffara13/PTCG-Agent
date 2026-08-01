
def test_matrix_transpose():
    x = np.arange(6).reshape((2, 3))
    actual = np.linalg.matrix_transpose(x)
    expected = x.T

    assert_equal(actual, expected)

    with assert_raises_regex(
        ValueError, "array must be at least 2-dimensional"
    ):
        np.linalg.matrix_transpose(x[:, 0])

