
def test_empty_matrix_rank():
    assert_equal(matrix_rank(np.zeros((0, 0))), 0)
    assert_equal(matrix_rank(np.zeros((0, 5))), 0)
    assert_equal(matrix_rank(np.zeros((5, 0))), 0)

    result = matrix_rank(np.zeros((0, 5, 5)))
    assert_equal(result.shape, (0,))
    assert_equal(result.dtype, np.intp)

    result = matrix_rank(np.zeros((3, 0, 5)))
    assert_equal(result, np.array([0, 0, 0]))

    result = matrix_rank(np.zeros((2, 5, 0)))
    assert_equal(result, np.array([0, 0]))

    result = matrix_rank(np.zeros((2, 3, 0, 4)))
    assert_equal(result.shape, (2, 3))
    assert_equal(result, np.zeros((2, 3), dtype=np.intp))

