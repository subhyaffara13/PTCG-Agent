
def test_onenorm_matrix_power_nnm():
    np.random.seed(1234)
    for n in range(1, 5):
        for p in range(5):
            M = np.random.random((n, n))
            Mp = np.linalg.matrix_power(M, p)
            observed = _onenorm_matrix_power_nnm(M, p)
            expected = np.linalg.norm(Mp, 1)
            assert_allclose(observed, expected)

