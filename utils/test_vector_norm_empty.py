
def test_vector_norm_empty():
    for dtype in [np.float64, np.float32, np.int32]:
        x = np.zeros(0, dtype)
        assert_equal(np.linalg.vector_norm(x, ord=1), 0)
        assert_equal(np.linalg.vector_norm(x, ord=2), 0)
        assert_equal(np.linalg.vector_norm(x, ord=np.inf), 0)

