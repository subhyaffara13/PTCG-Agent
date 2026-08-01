
def test_csr_getrow():
    N = 10
    np.random.seed(0)
    X = np.random.random((N, N))
    X[X > 0.7] = 0
    Xcsr = csr_matrix(X)

    for i in range(N):
        arr_row = X[i:i + 1, :]
        csr_row = Xcsr.getrow(i)

        assert_array_almost_equal(arr_row, csr_row.toarray())
        assert_(type(csr_row) is csr_matrix)

