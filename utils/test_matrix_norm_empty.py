
def test_matrix_norm_empty():
    for shape in [(0, 2), (2, 0), (0, 0)]:
        for dtype in [np.float64, np.float32, np.int32]:
            x = np.zeros(shape, dtype)
            assert_equal(np.linalg.matrix_norm(x, ord="fro"), 0)
            assert_equal(np.linalg.matrix_norm(x, ord="nuc"), 0)
            assert_equal(np.linalg.matrix_norm(x, ord=1), 0)
            assert_equal(np.linalg.matrix_norm(x, ord=2), 0)
            assert_equal(np.linalg.matrix_norm(x, ord=np.inf), 0)

